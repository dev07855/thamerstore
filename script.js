const translations = {
    "ar": {
        "welcome": "ارحب يا الفخمين نورتو باقاتنا القويه",
        "title": "اشتراكات مميزة",
        "langBtn": "English",
        "basic_title": "الباقة الأساسية",
        "golden_title": "الباقة الذهبية",
        "diamond_title": "باقة الماس",
        "rhodium_title": "باقة الروديوم",
        "period": "/ 12 شهر",
        "warranty_0": "0 أيام ضمان",
        "warranty_90": "90 يوم ضمان",
        "warranty_180": "180 ايام ضمان",
        "warranty_300": "300 ايام ضمان",
        "contact_btn": "تواصل معي للاشتراك",
        "footer_rights": "جميع الحقوق محفوظة © 2026",
        
        // Features
        "store_plus": "متجر بلس",
        "apps_5k": "اكثر من 5 الف تطبيق",
        "apps_7": "اكثر من 7 تطبيق",
        "apps_plus": "تطبيقات بلس",
        "games_hacked": "العاب مهكرة",
        "series_apps": "تطبيقات مسلسلات",
        "esign_yearly": "شهادة يساين (سنوي)",
        "gbox_yearly": "شهادة g box (سنوي)",
        "scarlet_yearly": "شهادة سكارليت (سنوي)",
        "warning_no_warranty": "تنبية هذة باقة مافي ضمان في حالة تعطل شهادة",
        "revoke_renew": "في حالة تعطل شهادة بعدها بيحتاج تجديد شتراك",
        "apps_plus_sat": "تطبيقات بلس(SAT +LRD+SY)",
        "apps_plus_sat_spaced": "تطبيقات بلس (SAT +LRD+SY)",
        "series_netflix_iptv": "تطبيقات مسلسلات+ نيت فليكس مجاني +iptv",
        "esign_gbox": "شهادة يساين + Gboks (سنوي)",
        "snap_plus_free": "سناب بلس مجاني",
        "warranty_3m": "ضمان 3 شهر في حالة تعطيل شهادة رح يتم تعويضك فوري 💯",
        "warranty_6m": "ضمان 6 شهر في حالة تعطيل شهادة رح يتم تعويضك فوري 💯",
        "warranty_10m": "ضمان 10 شهر في حالة تعطيل شهادة رح يتم تعويضك فوري 💯",
        "snap_free": "سناب مجاني",
        "kd_free": "تطبيقات kD مجاني",
        "revoke_comp": "في حالة تعطل شهادة بيتم تعويضك بشكل فوري",
        "support_24": "دعم فوري 24 ساعة",
        "support_tech_24": "دعم فني 24 ساعة",
        "sign_ipa": "اضافة تطبيقات توقيعة من خلال ipa",
        "sign_link": "توقيع تطبيقات من خلال رابط",
        "strong_features": "مميزات قوية علي باقة",
        "pubg_free": "ببجي مجاني",
        "billiard_free": "بليارد مجاني",
        "kr_mm_free": "العاب kr mm مجاني",
        "sifi_free": "العاب سيفي مجاني",
        "request_app": "طلب اي تطبيق و يتم اضافتة"
    },
    "en": {
        "welcome": "Welcome to our premium packages!",
        "title": "Premium Subscriptions",
        "langBtn": "العربية",
        "basic_title": "Basic Package",
        "golden_title": "Golden Package",
        "diamond_title": "Diamond Package",
        "rhodium_title": "Rhodium Package",
        "period": "/ 12 Months",
        "warranty_0": "0 Days Warranty",
        "warranty_90": "90 Days Warranty",
        "warranty_180": "180 Days Warranty",
        "warranty_300": "300 Days Warranty",
        "contact_btn": "Contact me to subscribe",
        "footer_rights": "All rights reserved © 2026",

        // Features
        "store_plus": "Plus Store",
        "apps_5k": "More than 5000 apps",
        "apps_7": "More than 7 apps",
        "apps_plus": "Plus Apps",
        "games_hacked": "Hacked Games",
        "series_apps": "Series Apps",
        "esign_yearly": "ESign Certificate (Yearly)",
        "gbox_yearly": "GBox Certificate (Yearly)",
        "scarlet_yearly": "Scarlet Certificate (Yearly)",
        "warning_no_warranty": "Note: No warranty if certificate is revoked",
        "revoke_renew": "Subscription renewal required if revoked",
        "apps_plus_sat": "Plus Apps (SAT +LRD+SY)",
        "apps_plus_sat_spaced": "Plus Apps (SAT +LRD+SY)",
        "series_netflix_iptv": "Series Apps + Free Netflix + IPTV",
        "esign_gbox": "ESign Certificate + Gboks (Yearly)",
        "snap_plus_free": "Free Snap Plus",
        "warranty_3m": "3 Months warranty, immediate compensation if revoked 💯",
        "warranty_6m": "6 Months warranty, immediate compensation if revoked 💯",
        "warranty_10m": "10 Months warranty, immediate compensation if revoked 💯",
        "snap_free": "Free Snapchat",
        "kd_free": "Free KD Apps",
        "revoke_comp": "Immediate compensation if certificate revoked",
        "support_24": "24/7 Immediate Support",
        "support_tech_24": "24/7 Technical Support",
        "sign_ipa": "Sign IPA apps",
        "sign_link": "Sign apps via reference link",
        "strong_features": "Powerful features included",
        "pubg_free": "Free PUBG",
        "billiard_free": "Free Billiards",
        "kr_mm_free": "Free KR MM Games",
        "sifi_free": "Free Sifi Games",
        "request_app": "Request any app to be added"
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const langBtn = document.querySelector('.lang-btn');
    let currentLang = localStorage.getItem('lang') || 'ar'; // Default to Arabic

    // Initial setup
    updateLanguage(currentLang);

    langBtn.addEventListener('click', (e) => {
        e.preventDefault();
        currentLang = currentLang === 'ar' ? 'en' : 'ar';
        updateLanguage(currentLang);
        localStorage.setItem('lang', currentLang);
    });
});

function updateLanguage(lang) {
    // 1. Update Direction and Lang attribute
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

    // 2. Update all text content based on exact matches or data-key attributes
    // Since we didn't add data-keys to HTML yet, we will try to match text content.
    // However, to be safe and accurate, let's map known text to keys.
    // PROPER WAY: We should have added data-key to HTML.
    // Let's do a hybrid: Iterate over all elements we know about.
    
    // NOTE: This part relies on the HTML structure not changing drastically or we need to add classes/ids.
    // To make this robust, I'll recommend we update the HTML to include data-i18n attributes.
    // But for now, let's use a "Text Walker" that replaces text node values if they match a known Arabic string (or English if switching back).
    
    // Actually, simply walking the DOM and replacing known strings is easiest for a quick fix without touching HTML structure deeply.
    
    const elements = document.querySelectorAll('body *');
    
    elements.forEach(element => {
        // Handle text nodes directly within elements (like <li>Text</li> or <h2>Text</h2>)
        Array.from(element.childNodes).forEach(node => {
            if (node.nodeType === 3 && node.nodeValue.trim() !== '') { // Text node
                const text = node.nodeValue.trim();
                const translationKey = findKeyByValue(text);
                
                if (translationKey) {
                    node.nodeValue = " " + translations[lang][translationKey] + " "; // Add spaces for safeguard
                }
            }
        });
    });

    // Handle specific complex elements manually if needed
    // Update Lang Button Text
    const langBtn = document.querySelector('.lang-btn');
    if (langBtn) {
        langBtn.innerHTML = translations[lang].langBtn + ' <i class="fas fa-globe"></i>';
    }
}

function findKeyByValue(text) {
    const arObj = translations['ar'];
    const enObj = translations['en'];
    
    // Check in Arabic dict
    for (let key in arObj) {
        if (arObj[key] === text || arObj[key].trim() === text.trim()) return key;
    }
    // Check in English dict (to allow switching back)
    for (let key in enObj) {
        if (enObj[key] === text || enObj[key].trim() === text.trim()) return key;
    }
    return null;
}
