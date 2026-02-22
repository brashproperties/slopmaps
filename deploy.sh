#!/bin/bash
# SLOPULATOR Quick Deploy Script
# Run this to deploy the SLOPULATOR to various platforms

echo "🏠💰 THE SLOPULATOR DEPLOYER 💰🏠"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found!"
    echo "Please run this script from the slopulator directory"
    exit 1
fi

echo "✅ Files found:"
ls -lh *.html *.css *.js 2>/dev/null | awk '{print "   ", $9, "(" $5 ")"}'
echo ""

echo "📦 Creating deployment package..."
tar -czf ../slopulator-deploy-$(date +%Y%m%d).tar.gz .
echo "✅ Package created: slopulator-deploy-$(date +%Y%m%d).tar.gz"
echo ""

echo "🚀 Deployment Options:"
echo ""
echo "1️⃣  GitHub Pages (FREE):"
echo "   - Create repo at github.com"
echo "   - Upload these files"
echo "   - Enable Pages in Settings"
echo ""
echo "2️⃣  Netlify Drop (FREE & INSTANT):"
echo "   - Go to https://app.netlify.com/drop"
echo "   - Drag and drop this folder"
echo "   - Get instant URL!"
echo ""
echo "3️⃣  Surge.sh (FREE):"
echo "   - npm install -g surge"
echo "   - surge --project . --domain slopulator.surge.sh"
echo ""
echo "4️⃣  Vercel (FREE):"
echo "   - npm install -g vercel"
echo "   - vercel --prod"
echo ""
echo "5️⃣  Any Web Host (FTP/cPanel):"
echo "   - Upload files to /public_html/slopulator/"
echo "   - Access at yourdomain.com/slopulator/"
echo ""

echo "🔧 Testing locally:"
echo "   python3 -m http.server 8765"
echo "   Then open http://localhost:8765"
echo ""

echo "✨ Done! Ready to SLOP!"
