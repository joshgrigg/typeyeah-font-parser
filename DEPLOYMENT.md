# Font Parser Service Deployment Guide

## Prerequisites

1. Vercel CLI installed: `npm i -g vercel`
2. Vercel account (sign up at https://vercel.com)

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

**Step 1: Navigate to the service directory**
```bash
cd services/font-parser
```

**Step 2: Initialize Vercel project (first time only)**
```bash
vercel
```

When prompted:
- **Set up and deploy?** → Y (Yes)
- **Which scope?** → Select your account/team
- **Link to existing project?** → N (No) - Create a new project
- **Project name?** → `font-parser` (or your preferred name)
- **In which directory is your code located?** → `./` (current directory)
- **Want to override settings?** → N (No) - Use detected settings

**Step 3: Deploy to production**
```bash
vercel --prod
```

**Step 4: Note the deployment URL**
The output will show something like:
```
✅ Production: https://font-parser-abc123.vercel.app
```

**Step 5: Add URL to Portal environment**

Add to your Portal app's environment variables (via Vercel dashboard or CLI):
```env
NEXT_PUBLIC_FONT_PARSER_URL=https://font-parser-abc123.vercel.app
```

### Option 2: Deploy via Vercel Dashboard

**Step 1: Push code to GitHub** (already done)

**Step 2: Import project in Vercel**
1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select `typeyeah` repository
4. Click "Import"

**Step 3: Configure project settings**
- **Project Name:** `font-parser`
- **Framework Preset:** Other
- **Root Directory:** `services/font-parser` ⚠️ **IMPORTANT**
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- **Install Command:** `pip install -r requirements.txt`

**Step 4: Deploy**
Click "Deploy" and wait for deployment to complete

**Step 5: Get deployment URL**
Copy the production URL (e.g., `https://font-parser.vercel.app`)

**Step 6: Configure Portal**
Add to Portal environment variables in Vercel:
1. Go to Portal project settings
2. Environment Variables section
3. Add: `NEXT_PUBLIC_FONT_PARSER_URL` = `https://font-parser-abc123.vercel.app`
4. Redeploy Portal

## Local Development

For local testing without deploying:

**Step 1: Install dependencies**
```bash
cd services/font-parser
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2: Run the service**
```bash
python main.py
```

Service runs at `http://localhost:8000`

**Step 3: Test the service**
```bash
# Health check
curl http://localhost:8000

# Parse a font file
curl -X POST http://localhost:8000/parse \
  -F "file=@path/to/font.ttf"
```

The Portal app automatically uses `http://localhost:8000` when `NEXT_PUBLIC_FONT_PARSER_URL` is not set.

## Troubleshooting

### Error: "The provided path does not exist"

**Cause:** You're trying to deploy from the wrong directory or with wrong project settings.

**Solution:**
1. Navigate to the font-parser directory: `cd services/font-parser`
2. Run `vercel --prod` from there
3. Or create a new Vercel project with root directory set to `services/font-parser`

### Error: Module not found during build

**Cause:** Python dependencies not installed correctly.

**Solution:**
1. Verify `requirements.txt` exists
2. Check Vercel build logs for Python version
3. Ensure all dependencies are listed in `requirements.txt`

### CORS errors in browser console

**Cause:** Portal domain not in CORS whitelist.

**Solution:**
1. Edit `main.py` in font-parser service
2. Add your Portal domain to `allow_origins` list:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3003",
    "https://your-portal-domain.vercel.app",
    "https://*.typeyeah.com"
]
```
3. Redeploy: `vercel --prod`

### Service returns 500 error

**Cause:** Font parsing error or missing dependencies.

**Solution:**
1. Check Vercel function logs: `vercel logs`
2. Test locally with the same font file
3. Verify font file format is supported (TTF, OTF, WOFF, WOFF2)

## Updating the Service

After making changes to the font-parser service:

```bash
cd services/font-parser
git add .
git commit -m "Update font parser service"
git push
vercel --prod
```

Vercel will automatically detect changes and redeploy.

## Environment Variables

The font-parser service does not require any environment variables. All configuration is in `main.py`.

The Portal app requires:
- `NEXT_PUBLIC_FONT_PARSER_URL` - URL of deployed font-parser service

## Monitoring

**Check deployment status:**
```bash
vercel ls
```

**View logs:**
```bash
vercel logs [deployment-url]
```

**View function logs in Vercel dashboard:**
1. Go to your font-parser project
2. Click on a deployment
3. Click "Functions" tab
4. View logs for each API call

## Production Checklist

Before going live:

- [ ] Deploy font-parser service to Vercel
- [ ] Note the production URL
- [ ] Add `NEXT_PUBLIC_FONT_PARSER_URL` to Portal environment
- [ ] Test font upload in Portal staging/preview
- [ ] Verify metadata extraction works
- [ ] Verify font matching returns results
- [ ] Check CORS is working (no browser errors)
- [ ] Test with various font formats (TTF, OTF, WOFF, WOFF2)
- [ ] Monitor Vercel function logs for errors
- [ ] Redeploy Portal with environment variable

## Cost Considerations

Vercel free tier includes:
- 100 GB bandwidth per month
- 100 hours function execution time
- 6,000 function invocations per day

Font parsing is relatively lightweight. Typical usage:
- ~1-2 seconds per font file
- ~1-5 MB per font file
- Should stay within free tier for moderate usage

For high volume (1000+ fonts/day), consider:
- Vercel Pro plan ($20/month)
- Or self-host on Railway, Render, or similar

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Test the service directly via curl
3. Verify CORS settings
4. Check Portal environment variables
5. Review this guide's troubleshooting section
