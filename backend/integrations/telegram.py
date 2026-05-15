"""
Hermes Business OS - Telegram Bot Integration
Voice, text, file handling, context routing
"""
import asyncio
from typing import Callable, Dict, Any, Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from core.config import settings
from app.skills.engine import SkillEngine


class TelegramBot:
    """Telegram bot interface for Hermes Business OS."""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application: Optional[Application] = None
        self.skill_engine = SkillEngine()
        self.message_handler: Optional[Callable] = None
    
    async def start(self):
        """Start the bot."""
        if not self.token:
            print("⚠️  Telegram bot token not configured")
            return
        
        self.application = Application.builder().token(self.token).build()
        
        # Register handlers
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        self.application.add_handler(CommandHandler("skills", self.cmd_skills))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        
        print("✅ Telegram bot started")
        
        # Start polling
        await self.application.initialize()
        await self.application.start_polling()
        await self.application.idle()
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome = (
            f"👋 ¡Hola! Soy tu asistente de *Hermes Business OS*.\n\n"
            f"Puedo ayudarte con:\n"
            f"• 📋 Gestión de clientes y cotizaciones\n"
            f"• 📅 Proyectos y tareas\n"
            f"• 📄 Generación de documentos\n"
            f"• 📊 Reportes y seguimientos\n\n"
            f"Simplemente dime qué necesitas.\n"
            f"Ejemplo: *'Cotiza un proyecto para Juan Pérez'*\n\n"
            f"Escribe /skills para ver mis habilidades."
        )
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "*Comandos disponibles:*\n\n"
            "/start - Iniciar conversación\n"
            "/skills - Ver habilidades disponibles\n"
            "/help - Mostrar esta ayuda\n\n"
            "*Ejemplos de uso:*\n"
            "• 'Registra cliente: Juan Pérez, juan@email.com'\n"
            "• 'Cotiza 10 horas de consultoría a $500/hora'\n"
            "• 'Crea proyecto Website Cliente X'\n"
            "• 'Genera reporte semanal'\n\n"
            "También puedes enviar *notas de voz* para registrar información."
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def cmd_skills(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /skills command."""
        skills = self.skill_engine.list_skills()
        
        text = "*Habilidades disponibles:*\n\n"
        for skill in skills:
            text += f"🔹 *{skill['name']}* (v{skill['version']})\n"
            text += f"   {skill['description']}\n"
            text += f"   Acciones: {skill['actions']}\n\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        text = update.message.text
        user_id = update.effective_user.id
        
        # Simple intent routing
        result = self.skill_engine.execute_by_intent(text)
        
        if result.get("success"):
            response = self._format_success(result)
        else:
            response = self._format_error(result, text)
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages."""
        await update.message.reply_text(
            "🎤 *Nota de voz recibida*\n\n"
            "En esta versión, transcribo notas de voz para que puedas "
            "registrar información mientras estás en el tráfico o en el campo.\n\n"
            "*(Transcripción en desarrollo - usar texto por ahora)*",
            parse_mode='Markdown'
        )
    
    def _format_success(self, result: Dict[str, Any]) -> str:
        """Format successful skill execution."""
        skill = result.get("skill", "")
        action = result.get("action", "")
        res = result.get("result", {})
        
        text = f"✅ *{skill.title()}* - {action.replace('_', ' ').title()}\n\n"
        
        if "mensaje" in res:
            text += f"{res['mensaje']}\n\n"
        
        if "cotizacion" in res:
            cot = res["cotizacion"]
            text += f"*Cliente:* {cot.get('cliente')}\n"
            text += f"*Total:* ${cot.get('total', 0):,.2f} {cot.get('moneda', 'MXN')}\n\n"
        
        if "siguiente_paso" in res:
            text += f"👉 *Siguiente paso:* {res['siguiente_paso']}"
        
        return text
    
    def _format_error(self, result: Dict[str, Any], original_text: str) -> str:
        """Format error response."""
        text = (
            f"🤔 No entendí bien: _\"{original_text}\"_\n\n"
            f"Intenta ser más específico o usa /skills para ver lo que puedo hacer.\n\n"
            f"*Ejemplos:*\n"
            f"• 'Cotiza servicios para Juan Pérez'\n"
            f"• 'Crea proyecto Nombre del Proyecto'\n"
            f"• 'Genera reporte semanal'"
        )
        return text


# Global instance
telegram_bot = TelegramBot()
