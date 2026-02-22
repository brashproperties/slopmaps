# THE SLOPULATOR - Deployment Instructions

## What is this?
A gloriously retro property evaluation tool with early 2000s Geocities aesthetic!

## Files Included
- `index.html` - The main HTML page (table-based layout, marquees, blinking text)
- `style.css` - Retro styling with animations, neon colors, sparkles
- `app.js` - Full functionality including visitor counter, calculations, bouncing emojis
- `.htaccess` - Apache configuration for clean URLs

## Deployment Options

### Option 1: Upload to brashproperties.com/slopulator

If you have FTP/cPanel access:

1. Create directory `/slopulator/` on your web server
2. Upload all 4 files to that directory
3. Access at: https://brashproperties.com/slopulator/

### Option 2: Squarespace (if that's your host)

Since brashproperties.com is on Squarespace, you have a few options:

**A) Code Injection (Simplest)**
1. Go to Squarespace Admin → Settings → Advanced → Code Injection
2. Create a new page at /slopulator
3. Add a Code Block with the full HTML/CSS/JS (might need to inline CSS/JS)

**B) Static File Upload**
Squarespace doesn't support direct file uploads to subdirectories easily.
You may need to use:
- GitHub Pages (free, see below)
- Netlify (free drag-and-drop deploy)
- Vercel (free)

### Option 3: GitHub Pages (Free Hosting)

1. Create a new GitHub repo: `slopulator`
2. Upload these files
3. Go to Settings → Pages → Enable
4. Access at: https://yourusername.github.io/slopulator

### Option 4: Netlify (Free)

1. Go to https://app.netlify.com/drop
2. Drag and drop the slopulator folder
3. Get instant URL!

## Features

✅ Property search with autocomplete (OpenStreetMap)
✅ ARV calculation (weighted average)
✅ Rental cashflow analysis
✅ Flip profit analysis with 70% rule
✅ Comparable sales (comps) display
✅ Save/load evaluations (localStorage)
✅ Visitor counter (retro digital style)
✅ Bouncing emojis with sparkles
✅ Confetti explosion on calculate
✅ Easter egg (click the house emoji!)
✅ Print/PDF support
✅ Mobile responsive (sort of)

## Browser Support

- Netscape Navigator 4.0 (just kidding... kind of)
- Chrome/Edge/Firefox/Safari (modern)
- Internet Explorer 6 (maybe, good luck)

## Known Issues

- Squarespace hosting may have limitations
- MIDI music placeholder (not implemented)
- Some Geocities GIFs may eventually disappear (hosted on archive.org)

## Made with 💖 for Bradley

Enjoy your gloriously weird SLOPULATOR!