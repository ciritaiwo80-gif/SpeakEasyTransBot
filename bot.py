import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from googletrans import Translator

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please add BOT_TOKEN in Railway Variables tab")
    exit(1)

print(f"✅ Token loaded successfully (length: {len(TOKEN)})")

# Initialize translator
translator = Translator()

# Supported languages dictionary
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ur': 'Urdu',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'sw': 'Swahili',
    'ha': 'Hausa',
    'yo': 'Yoruba',
    'ig': 'Igbo',
    'zu': 'Zulu',
    'af': 'Afrikaans',
    'am': 'Amharic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mn': 'Mongolian',
    'my': 'Myanmar',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'ug': 'Uyghur',
    'uk': 'Ukrainian',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
}

# User state tracking
user_target_lang = {}

# ===== Command Handlers =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_msg = (
        f"🌍 *Hello {user.first_name}!*\n\n"
        "Welcome to *SpeakEasyTransBot* - your language conversion companion!\n\n"
        "I can translate text between 100+ languages.\n\n"
        "*How to use:*\n"
        "1️⃣ Send /setlang to choose your target language\n"
        "2️⃣ Send me any text, and I'll translate it!\n\n"
        "Or use inline translation:\n"
        "• /en [text] - Translate to English\n"
        "• /es [text] - Translate to Spanish\n"
        "• /fr [text] - Translate to French\n\n"
        "Send /help to see all commands."
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_msg = (
        "📖 *SpeakEasyTransBot Help*\n\n"
        "*Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/setlang - Set your default target language\n"
        "/languages - List all supported languages\n"
        "/about - About this bot\n\n"
        "*Quick Translation:*\n"
        "• /en [text] - Translate to English\n"
        "• /es [text] - Translate to Spanish\n"
        "• /fr [text] - Translate to French\n"
        "• /de [text] - Translate to German\n"
        "• /it [text] - Translate to Italian\n"
        "• /pt [text] - Translate to Portuguese\n"
        "• /ru [text] - Translate to Russian\n"
        "• /zh [text] - Translate to Chinese\n"
        "• /ja [text] - Translate to Japanese\n"
        "• /ko [text] - Translate to Korean\n\n"
        "*Default Translation:*\n"
        "Set your default language with /setlang, then just send any text!"
    )
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def languages_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /languages command"""
    # Create a list of languages
    lang_list = "\n".join([f"• `{code}`: {name}" for code, name in list(LANGUAGES.items())[:20]])
    lang_msg = (
        f"📚 *Supported Languages (First 20)*\n\n"
        f"{lang_list}\n\n"
        f"*Total: {len(LANGUAGES)} languages*\n"
        f"Use /setlang to set your default language."
    )
    await update.message.reply_text(lang_msg, parse_mode='Markdown')

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setlang command - show language selection keyboard"""
    keyboard = []
    row = []
    for i, (code, name) in enumerate(LANGUAGES.items()):
        row.append(InlineKeyboardButton(name[:15], callback_data=f"lang_{code}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 *Select your default target language:*\n"
        "Choose a language from the list below. After setting, all texts you send will be translated to this language.",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_msg = (
        "🌍 *About SpeakEasyTransBot*\n\n"
        "This bot was created to help you translate text between 100+ languages.\n\n"
        "*Features:*\n"
        "✓ Supports 100+ languages\n"
        "✓ Set default target language\n"
        "✓ Quick translation commands\n"
        "✓ Privacy-focused (we don't store your text)\n"
        "✓ Free to use\n\n"
        "Built with ❤️ using googletrans and python-telegram-bot."
    )
    await update.message.reply_text(about_msg, parse_mode='Markdown')

# ===== Callback Query Handler =====
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection callback"""
    query = update.callback_query
    await query.answer()
    
    # Extract language code from callback data
    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, "Unknown")
    
    # Store user's language preference
    user_id = query.from_user.id
    user_target_lang[user_id] = lang_code
    
    await query.edit_message_text(
        f"✅ *Language set!*\n\n"
        f"Your default target language is now *{lang_name}*.\n\n"
        f"Just send me any text, and I'll translate it to {lang_name}!\n"
        f"Or use /help to see all commands.",
        parse_mode='Markdown'
    )

# ===== Translation Functions =====
async def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language"""
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"❌ Translation error: {str(e)}"

async def detect_language(text: str) -> str:
    """Detect language of text"""
    try:
        result = translator.detect(text)
        return result.lang
    except Exception as e:
        return "unknown"

# ===== Message Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    text = update.message.text
    
    if text.startswith('/'):
        return
    
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to translate!")
        return
    
    # Check if user has set a default language
    user_id = update.effective_user.id
    target_lang = user_target_lang.get(user_id, 'en')  # Default to English
    
    # Detect source language
    source_lang = await detect_language(text)
    source_name = LANGUAGES.get(source_lang, "Unknown")
    target_name = LANGUAGES.get(target_lang, "Unknown")
    
    # Translate
    translated_text = await translate_text(text, target_lang)
    
    # Format response
    response = (
        f"🌍 *Translation*\n"
        f"{'─' * 25}\n"
        f"🔹 *From:* {source_name}\n"
        f"🔸 *To:* {target_name}\n"
        f"{'─' * 25}\n"
        f"📝 *Translation:*\n"
        f"{translated_text}\n"
        f"{'─' * 25}\n"
        f"💡 *Tip:* Use /setlang to change language\n"
        f"   Use /help for all commands"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

# ===== Quick Translation Command Handlers =====
async def quick_translate(update: Update, context: ContextTypes.DEFAULT_TYPE, target_lang: str):
    """Handle quick translation commands like /en, /es, etc."""
    # Get the text after the command
    command_text = update.message.text
    parts = command_text.split(' ', 1)
    
    if len(parts) < 2:
        lang_name = LANGUAGES.get(target_lang, "Unknown")
        await update.message.reply_text(
            f"⚠️ Please provide text to translate to {lang_name}.\n"
            f"Example: `/{target_lang} Hello world`",
            parse_mode='Markdown'
        )
        return
    
    text_to_translate = parts[1].strip()
    if not text_to_translate:
        await update.message.reply_text("⚠️ Please provide text to translate!")
        return
    
    translated_text = await translate_text(text_to_translate, target_lang)
    source_lang = await detect_language(text_to_translate)
    source_name = LANGUAGES.get(source_lang, "Unknown")
    target_name = LANGUAGES.get(target_lang, "Unknown")
    
    response = (
        f"🌍 *Quick Translation*\n"
        f"{'─' * 25}\n"
        f"🔹 *From:* {source_name}\n"
        f"🔸 *To:* {target_name}\n"
        f"{'─' * 25}\n"
        f"📝 *Translation:*\n"
        f"{translated_text}"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

# Create quick translation handlers
def create_quick_handler(lang_code):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await quick_translate(update, context, lang_code)
    return handler

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    print(f"❌ Error: {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")

# ===== Main Function =====
def main():
    """Start the bot"""
    print("🚀 Starting SpeakEasyTransBot...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application built successfully")
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("languages", languages_command))
        application.add_handler(CommandHandler("setlang", setlang_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Add quick translation handlers
        quick_langs = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi']
        for lang in quick_langs:
            application.add_handler(CommandHandler(lang, create_quick_handler(lang)))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running! Waiting for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
