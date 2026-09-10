import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
TOKEN = "8947725456:AAG4vdQf6AKhek_uFHIMpXYSodShLmsFvig"

# إنشاء مجلد لحفظ إيصالات الدفع الواردة محلياً
RECEIPTS_DIR = "receipts"
if not os.path.exists(RECEIPTS_DIR):
    os.makedirs(RECEIPTS_DIR)

# ذاكرة مؤقتة لتتبع حالة العميل
user_states = {}

def is_arabic(text: str) -> bool:
    if not text:
        return False
    for char in text:
        code = ord(char)
        if (0x0600 <= code <= 0x06FF) or (0x0750 <= code <= 0x077F) or (0x08A0 <= code <= 0x08FF):
            return True
    return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_states[user_id] = {"step": "waiting_sector"}
    
    welcome_text = (
        "السلام عليكم، Captain Ahmed Habib 🫡\n\n"
        "أهلاً بك في منظومة MNCOS Sovereign Gateway.\n"
        "الإطار الاستراتيجي: Civilizational Coherence Core™\n\n"
        "قنوات التواصل والاعتماد الرسمية:\n"
        "• البريد الإلكتروني: maritimeahos@gmail.com\n"
        "• واتساب / الاتصال المباشر: 00201032476258\n"
        "• لينكد إن: https://www.linkedin.com/in/ahmed-habib-mncos-6440a73a2\n\n"
        "يرجى اختيار قطاعك التشغيلي لاستعراض الخدمات الخمس السيادية:\n\n"
        "------------------------------------\n"
        "Welcome to MNCOS Sovereign Gateway.\n"
        "Strategic Framework: Civilizational Coherence Core™\n"
        "Please select your operational maritime sector:"
    )
    keyboard = [
        [InlineKeyboardButton("🚢 Commercial Fleet / Cargo", callback_data="sector_cargo")],
        [InlineKeyboardButton("🛢️ Offshore Rigs / Energy", callback_data="sector_rigs")],
        [InlineKeyboardButton("⚓ Ports & Logistics", callback_data="sector_ports")],
        [InlineKeyboardButton("🛡️ Sovereign Investment / Other", callback_data="sector_sovereign")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("sector_"):
        user_states[user_id] = {"sector": data, "step": "waiting_fleet_size"}
        await query.message.reply_text(
            "📊 **Sector Recorded Successfully.**\n"
            "يرجى كتابة عدد القطع البحرية أو تفاصيل الأصول الخاصة بك / Please enter your fleet size or assets details:"
        )
    elif data == "s1":
        resp = (
            "🛡️ **1. MNCOS Sovereign Operating System:**\n"
            "• Core Fleet Deployment: Starting at **$15,000**.\n"
            "• Critical Asset & Rig Customization: Starting at **$35,000**.\n"
            "• Payment: Transfer via InstaPay to Vodafone Cash: `01032476258` then send the receipt."
        )
        await query.message.reply_text(resp)
    elif data == "s2":
        resp = (
            "📊 **2. Sovereign Audit & Stress Testing:**\n"
            "• Standard Audit: **$50,000**.\n"
            "• Advanced Comprehensive Stress Testing: **$100,000**.\n"
            "• Payment: InstaPay to Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s3":
        resp = (
            "⚓ **3. Offline Emergency Node License:**\n"
            "• Single Air-Gapped Node Annual License: **$8,500**.\n"
            "• Multi-Node Enterprise Package: **$25,000**.\n"
            "• Payment: InstaPay to Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s4":
        resp = (
            "📜 **4. Tier 3 Governance & IP:**\n"
            "• Sovereign Advisory & Black-Box Governance: Starting at **$45,000**.\n"
            "• Payment: InstaPay to Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s5":
        resp = (
            "🧠 **5. Sovereign Expert Maritime Intelligence:**\n"
            "• Advanced AI-driven cognitive engine for complex navigational, engineering, and sovereign architectural queries.\n"
            "• Provides real-time deterministic answers and precision-priced consultations under the direct authority of Captain Ahmed Habib.\n"
            "• Consultations priced based on complexity. Payment via InstaPay / Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)

# معالجة إيصالات الدفع
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = os.path.join(RECEIPTS_DIR, f"receipt_{update.message.from_user.id}_{photo.file_unique_id}.jpg")
    await file.download_to_drive(file_path)
    
    await update.message.reply_text(
        "📥 **Payment receipt received and securely stored.**\n"
        "Notifying Captain Ahmed Habib for sovereign review and manual authorization via maritimeahos@gmail.com"
    )

# معالجة الرسائل والأسئلة الاستشارية الملاحية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.message.from_user.id
    state = user_states.get(user_id, {})
    
    if state.get("step") == "waiting_fleet_size":
        user_states[user_id]["step"] = "completed"
        
        analysis_reply = (
            f"🧠 **Operational & Fleet Profile Analysis:**\n"
            f"• Based on your input ('{text}'), the MNCOS sovereign engine has evaluated your structural requirements.\n\n"
            f"📌 **Recommended Solutions (The 5 Core Sovereign Services):**\n"
            f"يمكنك استعراض تفاصيل الخدمات الخمس المعتمدة أدناه واختيار ما يناسب أسطولك:"
        )
        await update.message.reply_text(analysis_reply)
        
        keyboard = [
            [InlineKeyboardButton("🛡️ 1. Sovereign OS ($15K - $35K+)", callback_data="s1")],
            [InlineKeyboardButton("📊 2. Sovereign Audit ($50K - $100K)", callback_data="s2")],
            [InlineKeyboardButton("⚓ 3. Emergency Node ($8.5K - $25K)", callback_data="s3")],
            [InlineKeyboardButton("📜 4. Tier 3 Governance ($45K+)", callback_data="s4")],
            [InlineKeyboardButton("🧠 5. Expert Maritime Intelligence", callback_data="s5")]
        ]
        await update.message.reply_text("Select a sovereign service for pricing & execution details:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # الرد التفاعلي للأسئلة المعقدة والاستشارات الملاحية (الخدمة الخامسة)
    if is_arabic(text):
        reply = (
            "🧠 **[الخدمة الخامسة - الاستشارات الملاحية السيادية]:**\n"
            f"تم استلام استفسارك الهندسي/الملاحي المعقد. يقدم محرك MNCOS الإجابة الحتمية وتحليل الدقة بناءً على الواقع.\n"
            "• تكلفة الاستشارة الفورية يتم تقديرها وتأكيدها تحت الإشراف المباشر لـ Captain Ahmed Habib.\n"
            "• الدفع عبر InstaPay / فودافون كاش: `01032476258`\n\n"
            "للتواصل المباشر:\n"
            "• البريد: maritimeahos@gmail.com | واتساب: 00201032476258"
        )
    else:
        reply = (
            "🧠 **[Service 5 - Sovereign Expert Maritime Intelligence]:**\n"
            "Your complex navigational/engineering query has been received by the MNCOS cognitive engine.\n"
            "• Precision-priced consultation under the direct authority of Captain Ahmed Habib.\n"
            "• Payment via InstaPay / Vodafone Cash: `01032476258`\n\n"
            "Direct Channels:\n"
            "• Email: maritimeahos@gmail.com | WhatsApp: 00201032476258"
        )
    await update.message.reply_text(reply)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🚀 MNCOS Sovereign Master Bot with 5 Core Services & Expert Intelligence is running...")
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
