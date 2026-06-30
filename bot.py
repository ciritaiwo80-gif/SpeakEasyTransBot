import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from deep_translator import GoogleTranslator

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please add BOT_TOKEN in Railway Variables tab")
    exit(1)

print(f"✅ Token loaded successfully (length: {len(TOKEN)})")

# Language mapping
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-CN': 'Chinese (Simplified)',
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
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
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
    'sv': 'Swedish',
    'tg': 'Tajik',
    'tt': 'Tatar',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'ug': 'Uyghur',
    'uk': 'Ukrainian',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish'
}

# User state storage
user_target_lang = {}

# ===== Translation Function =====
def translate_text(text: str, target_lang: str) -> str:
    """Translate text using GoogleTranslator with error handling"""
    try:
        # Detect source language
        translator = GoogleTranslator(target=target_lang)
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"Translation error: {e}")
        # Try alternative approach
        try:
            # Sometimes works with source='auto'
            translator = GoogleTranslator(source='auto', target=target_lang)
            return translator.translate(text)
        except Exception as e2:
            print(f"Alternative translation error: {e2}")
            return f"⚠️ Translation failed: {str(e2)}"

def detect_language(text: str) -> str:
    """Detect language of text"""
    try:
        result = GoogleTranslator().detect(text)
        return result
    except:
        return 'en'  # Default to English if detection fails

# ===== Command Handlers =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    lang_list = "\n".join([f"• `{code}`: {name}" for code, name in list(LANGUAGES.items())[:20]])
    lang_msg = (
        f"📚 *Supported Languages (First 20)*\n\n"
        f"{lang_list}\n\n"
        f"*Total: {len(LANGUAGES)} languages*\n"
        f"Use /setlang to set your default language."
    )
    await update.message.reply_text(lang_msg, parse_mode='Markdown')

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "🌍 *Select your default target language:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_msg = (
        "🌍 *About SpeakEasyTransBot*\n\n"
        "This bot was created to help you translate text between 100+ languages.\n\n"
        "*Features:*\n"
        "✓ Supports 100+ languages\n"
        "✓ Set default target language\n"
        "✓ Quick translation commands\n"
        "✓ Privacy-focused (we don't store your text)\n"
        "✓ Free to use\n\n"
        "Built with ❤️ using deep-translator and python-telegram-bot."
    )
    await update.message.reply_text(about_msg, parse_mode='Markdown')

# ===== Callback Handler =====
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, "Unknown")
    
    user_id = query.from_user.id
    user_target_lang[user_id] = lang_code
    
    await query.edit_message_text(
        f"✅ *Language set!*\n\n"
        f"Your default target language is now *{lang_name}*.\n\n"
        f"Just send me any text, and I'll translate it to {lang_name}!",
        parse_mode='Markdown'
    )

# ===== Message Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text.startswith('/'):
        return
    
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to translate!")
        return
    
    # Get user's default language
    user_id = update.effective_user.id
    target_lang = user_target_lang.get(user_id, 'en')
    
    try:
        # Translate
        translated = translate_text(text, target_lang)
        source_lang = detect_language(text)
        
        source_name = LANGUAGES.get(source_lang, "Unknown")
        target_name = LANGUAGES.get(target_lang, "Unknown")
        
        response = (
            f"🌍 *Translation*\n"
            f"{'─' * 25}\n"
            f"🔹 *From:* {source_name}\n"
            f"🔸 *To:* {target_name}\n"
            f"{'─' * 25}\n"
            f"📝 *Translation:*\n"
            f"{translated}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Handler error: {e}")
        await update.message.reply_text(f"⚠️ Translation error: {str(e)}")

# ===== Quick Translation Handlers =====
async def quick_translate(update: Update, context: ContextTypes.DEFAULT_TYPE, target_lang: str):
    parts = update.message.text.split(' ', 1)
    
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
    
    try:
        translated = translate_text(text_to_translate, target_lang)
        source_lang = detect_language(text_to_translate)
        
        source_name = LANGUAGES.get(source_lang, "Unknown")
        target_name = LANGUAGES.get(target_lang, "Unknown")
        
        response = (
            f"🌍 *Quick Translation*\n"
            f"{'─' * 25}\n"
            f"🔹 *From:* {source_name}\n"
            f"🔸 *To:* {target_name}\n"
            f"{'─' * 25}\n"
            f"📝 *Translation:*\n"
            f"{translated}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Quick translate error: {e}")
        await update.message.reply_text(f"⚠️ Translation error: {str(e)}")

def create_quick_handler(lang_code):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await quick_translate(update, context, lang_code)
    return handler

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ Error: {context.error}")
    try:
        if update and update.message:
            await update.message.reply_text("⚠️ An error occurred. Please try again.")
    except:
        pass

# ===== Main Function =====
def main():
    print("🚀 Starting SpeakEasyTransBot...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application built successfully")
        
        # Command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("languages", languages_command))
        application.add_handler(CommandHandler("setlang", setlang_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Quick translation handlers
        quick_langs = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi']
        for lang in quick_langs:
            application.add_handler(CommandHandler(lang, create_quick_handler(lang)))
        
        # Callback handler
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running! Waiting for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
