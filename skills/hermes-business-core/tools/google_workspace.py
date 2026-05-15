"""
Hermes Business OS — Google Workspace Integration
Tools for interacting with Google Sheets, Drive, Docs, and Calendar.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Google API imports (optional — graceful degradation if not installed)
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from .config_loader import get_config
except ImportError:
    from config_loader import get_config


class GoogleWorkspace:
    """Integration with Google Workspace APIs."""
    
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/calendar",
    ]
    
    def __init__(self):
        self.config = get_config()
        self.credentials = None
        self.services = {}
        self._initialized = False
        
    def _init_credentials(self) -> bool:
        """Initialize Google API credentials."""
        if not GOOGLE_AVAILABLE:
            return False
        
        if self.credentials:
            return True
        
        # Find service account file
        service_account_path = self._find_service_account()
        if not service_account_path:
            return False
        
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=self.SCOPES
            )
            return True
        except Exception as e:
            print(f"⚠️  Failed to load Google credentials: {e}")
            return False
    
    def _find_service_account(self) -> Optional[Path]:
        """Find the service account JSON file."""
        config_path = self.config.get("integraciones.google_workspace.cuenta_servicio")
        
        if config_path:
            # Try relative to project root
            project_root = Path(__file__).parent.parent.parent.parent.parent
            full_path = project_root / config_path
            if full_path.exists():
                return full_path
            
            # Try absolute path
            if Path(config_path).exists():
                return Path(config_path)
        
        # Try common locations
        for filename in ["google-service-account.json", "service-account.json"]:
            for location in [
                Path.cwd(),
                Path.cwd() / "config",
                Path.home() / ".hermes-business-os" / "config",
            ]:
                candidate = location / filename
                if candidate.exists():
                    return candidate
        
        return None
    
    def _get_service(self, api_name: str, version: str):
        """Get or create a Google API service."""
        key = f"{api_name}:{version}"
        
        if key not in self.services:
            if not self._init_credentials():
                return None
            
            try:
                self.services[key] = build(api_name, version, credentials=self.credentials)
            except Exception as e:
                print(f"⚠️  Failed to create {api_name} service: {e}")
                return None
        
        return self.services[key]
    
    # === Sheets ===
    
    def get_sheets_service(self):
        """Get Google Sheets API service."""
        return self._get_service("sheets", "v4")
    
    def create_spreadsheet(self, title: str) -> Optional[str]:
        """Create a new Google Spreadsheet. Returns spreadsheet ID."""
        service = self.get_sheets_service()
        if not service:
            return None
        
        try:
            spreadsheet = {"properties": {"title": title}}
            result = service.spreadsheets().create(body=spreadsheet).execute()
            return result.get("spreadsheetId")
        except HttpError as e:
            print(f"⚠️  Failed to create spreadsheet: {e}")
            return None
    
    def get_spreadsheet_values(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """Get values from a spreadsheet range."""
        service = self.get_sheets_service()
        if not service:
            return []
        
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            return result.get("values", [])
        except HttpError as e:
            print(f"⚠️  Failed to get values: {e}")
            return []
    
    def update_spreadsheet_values(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> bool:
        """Update values in a spreadsheet range."""
        service = self.get_sheets_service()
        if not service:
            return False
        
        try:
            body = {"values": values}
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            return True
        except HttpError as e:
            print(f"⚠️  Failed to update values: {e}")
            return False
    
    def append_spreadsheet_values(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> bool:
        """Append values to a spreadsheet."""
        service = self.get_sheets_service()
        if not service:
            return False
        
        try:
            body = {"values": values}
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()
            return True
        except HttpError as e:
            print(f"⚠️  Failed to append values: {e}")
            return False
    
    # === Drive ===
    
    def get_drive_service(self):
        """Get Google Drive API service."""
        return self._get_service("drive", "v3")
    
    def create_folder(self, name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """Create a folder in Google Drive. Returns folder ID."""
        service = self.get_drive_service()
        if not service:
            return None
        
        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        
        if parent_id:
            metadata["parents"] = [parent_id]
        
        try:
            result = service.files().create(body=metadata, fields="id").execute()
            return result.get("id")
        except HttpError as e:
            print(f"⚠️  Failed to create folder: {e}")
            return None
    
    def find_folder(self, name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """Find a folder by name. Returns folder ID or None."""
        service = self.get_drive_service()
        if not service:
            return None
        
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
        
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        try:
            results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
            files = results.get("files", [])
            
            if files:
                return files[0].get("id")
            return None
        except HttpError as e:
            print(f"⚠️  Failed to find folder: {e}")
            return None
    
    def get_or_create_folder(self, name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """Get existing folder or create new one."""
        folder_id = self.find_folder(name, parent_id)
        if folder_id:
            return folder_id
        return self.create_folder(name, parent_id)
    
    # === Docs ===
    
    def get_docs_service(self):
        """Get Google Docs API service."""
        return self._get_service("docs", "v1")
    
    def create_document(self, title: str) -> Optional[str]:
        """Create a new Google Doc. Returns document ID."""
        service = self.get_docs_service()
        if not service:
            return None
        
        try:
            result = service.documents().create(body={"title": title}).execute()
            return result.get("documentId")
        except HttpError as e:
            print(f"⚠️  Failed to create document: {e}")
            return None
    
    # === Calendar ===
    
    def get_calendar_service(self):
        """Get Google Calendar API service."""
        return self._get_service("calendar", "v3")
    
    def create_event(self, calendar_id: str, summary: str, start: str, end: str, 
                     description: str = "", attendees: List[str] = None) -> Optional[str]:
        """Create a calendar event. Returns event ID."""
        service = self.get_calendar_service()
        if not service:
            return None
        
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start},
            "end": {"dateTime": end},
        }
        
        if attendees:
            event["attendees"] = [{"email": e} for e in attendees]
        
        try:
            result = service.events().insert(calendarId=calendar_id, body=event).execute()
            return result.get("id")
        except HttpError as e:
            print(f"⚠️  Failed to create event: {e}")
            return None


# Singleton instance
_gw_instance = None


def get_google_workspace() -> GoogleWorkspace:
    """Get or create singleton Google Workspace instance."""
    global _gw_instance
    if _gw_instance is None:
        _gw_instance = GoogleWorkspace()
    return _gw_instance
