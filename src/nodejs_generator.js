const nodeHtmlToImage = require('node-html-to-image');
const Handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');

// HTML template with CSS styling
const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            width: 1080px;
            height: 1350px;
            background: linear-gradient(135deg, #ff6b6b, #ff5252);
            font-family: 'Noto Sans Arabic', Arial, sans-serif;
            position: relative;
            overflow: hidden;
        }
        
        .background-pattern {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.1;
            background-image: radial-gradient(circle at 25% 25%, white 2px, transparent 2px),
                              radial-gradient(circle at 75% 75%, white 2px, transparent 2px);
            background-size: 50px 50px;
        }
        
        .hero-layout {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            text-align: center;
        }
        
        .text-panel {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 60px;
        }
        
        .headline {
            font-size: 48px;
            font-weight: 700;
            color: white;
            margin-bottom: 20px;
            direction: rtl;
            text-align: center;
        }
        
        .subheadline {
            font-size: 32px;
            color: white;
            opacity: 0.9;
            direction: rtl;
            text-align: center;
        }
        
        .coats-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .coat {
            width: 80px;
            height: 120px;
            border-radius: 10px;
            position: relative;
            border: 3px solid white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .coat:nth-child(1) { background: #FF6B6B; }
        .coat:nth-child(2) { background: #4ECDC4; }
        .coat:nth-child(3) { background: #45B7D1; }
        .coat:nth-child(4) { background: #96CEB4; }
        .coat:nth-child(5) { background: #FFEAA7; }
        
        .coat::before {
            content: '';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 20px;
            height: 10px;
            border: 3px solid #666;
            border-bottom: none;
            border-radius: 10px 10px 0 0;
        }
        
        .brand {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 24px;
            font-weight: 600;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <div class="background-pattern"></div>
    <div class="hero-layout">
        <div class="text-panel">
            <div class="headline">{{headline}}</div>
            <div class="subheadline">{{subheadline}}</div>
        </div>
        <div class="coats-container">
            <div class="coat"></div>
            <div class="coat"></div>
            <div class="coat"></div>
            <div class="coat"></div>
            <div class="coat"></div>
        </div>
    </div>
    {{#if brand}}<div class="brand">{{brand}}</div>{{/if}}
</body>
</html>
`;

async function generateSocialImage(content, outputPath) {
    const template = Handlebars.compile(htmlTemplate);
    const html = template(content);
    
    const image = await nodeHtmlToImage({
        html: html,
        quality: 100,
        type: 'png',
        puppeteerArgs: {
            args: ['--no-sandbox'],
        },
        encoding: 'buffer'
    });
    
    fs.writeFileSync(outputPath, image);
    console.log(`Generated: ${outputPath}`);
}

async function main() {
    const content = {
        headline: 'کت‌های زمستانی جدید',
        subheadline: 'مجموعه‌ای از بهترین طراحی‌ها',
        brand: 'Fashion Store'
    };
    
    const outputDir = path.join(__dirname, '..', 'output');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const outputPath = path.join(outputDir, 'nodejs_social_post.png');
    await generateSocialImage(content, outputPath);
    console.log('Node.js image generation completed!');
}

if (require.main === module) {
    main().catch(console.error);
}
