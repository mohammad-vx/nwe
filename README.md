

```markdown
# VideoSegmentPro

أداة سطر أوامر متقدمة لتحليل وتقطيع وتحرير مقاطع الفيديو مع دعم كامل للترجمات العربية.

## المميزات الرئيسية

- تحليل تلقائي للفيديو لاكتشاف أفضل نقاط القطع
- دعم الترجمات العربية (SRT)
- تحرير المقاطع المعالجة
- قص وتعديل أبعاد الفيديو
- حفظ إعدادات المشروع
- واجهة مستخدم تفاعلية
- تخزين مؤقت للتحليلات لتحسين الأداء

## المتطلبات

```bash
pip install -r requirements.txt
```

- FFmpeg (يجب تثبيته على النظام)
- Python 3.8+
- moviepy
- pydub
- numpy

## طريقة الاستخدام

1. قم بتشغيل البرنامج:
```bash
python video_segment_pro.py
```

2. القائمة الرئيسية تتضمن:
   - تحليل الفيديو للمقاطع
   - إنشاء مقطع مخصص
   - تحرير مقطع موجود
   - الإعدادات

3. الإعدادات المتاحة:
   - مجلد المخرجات
   - المدة الزمنية (الحد الأدنى والأقصى)
   - إعدادات القص
   - جودة الفيديو
   - معدل البت

## أمثلة الاستخدام

```python
# تحليل فيديو وتقطيعه تلقائياً
python video_segment_pro.py --video path/to/video.mp4

# إضافة ترجمة
python video_segment_pro.py --video video.mp4 --srt subtitles.srt

# تخصيص مجلد المخرجات
python video_segment_pro.py --output custom/output/path
```

## المساهمة

نرحب بمساهماتكم! يرجى:
1. عمل Fork للمشروع
2. إنشاء فرع للميزة: `git checkout -b feature/amazing-feature`
3. commit التغييرات: `git commit -m 'Add amazing feature'`
4. رفع الفرع: `git push origin feature/amazing-feature`
5. فتح Pull Request

## الترخيص

هذا المشروع مرخص تحت MIT License - انظر ملف LICENSE للتفاصيل

## الإقرارات

- FFmpeg للمعالجة الأساسية للفيديو
- moviepy لتحليل الفيديو
- pydub لتحليل الصوت
```

خطوات رفع المشروع على GitHub:

1. أنشئ مستودع جديد على GitHub باسم `VideoSegmentPro`

2. قم بتنظيم الملفات المحلية:
```bash
VideoSegmentPro/
├── video_segment_pro.py  # الملف الرئيسي
├── requirements.txt      # المتطلبات
├── README.md            # الشرح
└── LICENSE             # رخصة MIT
```

3. أضف ملف requirements.txt:
```text
moviepy>=1.0.3
pydub>=0.25.1
numpy>=1.21.0
```

4. قم بتنفيذ الأوامر التالية:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/VideoSegmentPro.git
git push -u origin main
```

5. تأكد من إضافة ملف .gitignore:
```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Project specific
processed_videos.json
output/
```

