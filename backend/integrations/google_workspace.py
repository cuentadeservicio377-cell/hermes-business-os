"""
Hermes Business OS - Google Workspace Integration
Sheets, Docs, Slides, Drive, Calendar
"""
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.config import settings


class GoogleWorkspaceIntegration:
    """Integration with Google Workspace APIs."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/presentations',
        'https://www.googleapis.com/auth/calendar'
    ]
    
    def __init__(self):
        self.credentials = None
        self.services = {}
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with service account."""
        creds_path = settings.GOOGLE_SERVICE_ACCOUNT_JSON
        if not creds_path or not Path(creds_path).exists():
            print("⚠️  Google service account not configured")
            return
        
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=self.SCOPES
            )
            print("✅ Google Workspace authenticated")
        except Exception as e:
            print(f"⚠️  Google auth failed: {e}")
    
    def _get_service(self, api_name: str, version: str):
        """Get or create a Google API service."""
        if not self.credentials:
            return None
        
        key = f"{api_name}_{version}"
        if key not in self.services:
            self.services[key] = build(api_name, version, credentials=self.credentials)
        return self.services[key]
    
    # === Sheets ===
    
    def sheets_read(self, spreadsheet_id: str, range_name: str) -> List[List]:
        """Read data from a Google Sheet."""
        service = self._get_service('sheets', 'v4')
        if not service:
            return []
        
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as e:
            print(f"Sheets read error: {e}")
            return []
    
    def sheets_write(self, spreadsheet_id: str, range_name: str, 
                     values: List[List]) -> bool:
        """Write data to a Google Sheet."""
        service = self._get_service('sheets', 'v4')
        if not service:
            return False
        
        try:
            body = {'values': values}
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=range_name,
                valueInputOption='RAW', body=body
            ).execute()
            return True
        except HttpError as e:
            print(f"Sheets write error: {e}")
            return False
    
    def sheets_create(self, title: str) -> Optional[str]:
        """Create a new Google Sheet."""
        service = self._get_service('sheets', 'v4')
        if not service:
            return None
        
        try:
            spreadsheet = {'properties': {'title': title}}
            result = service.spreadsheets().create(body=spreadsheet).execute()
            return result.get('spreadsheetId')
        except HttpError as e:
            print(f"Sheets create error: {e}")
            return None
    
    # === Docs ===
    
    def docs_create(self, title: str, content: str = None) -> Optional[str]:
        """Create a new Google Doc."""
        service = self._get_service('docs', 'v1')
        if not service:
            return None
        
        try:
            doc = {'title': title}
            result = service.documents().create(body=doc).execute()
            doc_id = result.get('documentId')
            
            if content:
                self.docs_append(doc_id, content)
            
            return doc_id
        except HttpError as e:
            print(f"Docs create error: {e}")
            return None
    
    def docs_append(self, doc_id: str, text: str) -> bool:
        """Append text to a Google Doc."""
        service = self._get_service('docs', 'v1')
        if not service:
            return False
        
        try:
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': text
                }
            }]
            service.documents().batchUpdate(
                documentId=doc_id, body={'requests': requests}
            ).execute()
            return True
        except HttpError as e:
            print(f"Docs append error: {e}")
            return False
    
    # === Drive ===
    
    def drive_upload(self, file_path: str, folder_id: str = None) -> Optional[str]:
        """Upload a file to Google Drive."""
        from googleapiclient.http import MediaFileUpload
        
        service = self._get_service('drive', 'v3')
        if not service:
            return None
        
        try:
            file_metadata = {'name': Path(file_path).name}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path)
            result = service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()
            return result.get('id')
        except HttpError as e:
            print(f"Drive upload error: {e}")
            return None
    
    def drive_create_folder(self, name: str, parent_id: str = None) -> Optional[str]:
        """Create a folder in Google Drive."""
        service = self._get_service('drive', 'v3')
        if not service:
            return None
        
        try:
            metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                metadata['parents'] = [parent_id]
            
            result = service.files().create(body=metadata, fields='id').execute()
            return result.get('id')
        except HttpError as e:
            print(f"Drive folder error: {e}")
            return None


# Global instance
google_workspace = GoogleWorkspaceIntegration()
