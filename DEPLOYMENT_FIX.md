# Deployment Fix for pkg_resources Error

## Problem
The `razorpay==1.4.1` package requires `pkg_resources` which is part of `setuptools`, but it's not being installed properly in Python 3.14.

## Solution Options

### Option 1: Update requirements.txt (RECOMMENDED - Already Done)
The `requirements.txt` has been updated to include:
```
setuptools>=65.5.0
```

**Action Required:**
1. Commit and push the changes:
```bash
git add requirements.txt routes/ utils/
git commit -m "Fix pkg_resources error by adding setuptools and making razorpay optional"
git push
```

2. Render will automatically redeploy with the fix

---

### Option 2: Update Build Command in Render (Backup Solution)

If Option 1 doesn't work, update the build command in Render dashboard:

**Current Build Command:**
```bash
pip install -r requirements.txt
```

**New Build Command:**
```bash
pip install setuptools>=65.5.0 && pip install -r requirements.txt
```

**Steps:**
1. Go to Render dashboard
2. Click your web service
3. Go to "Settings"
4. Find "Build Command"
5. Update it to the new command above
6. Click "Save Changes"
7. Trigger a manual deploy

---

### Option 3: Downgrade Python Version (If all else fails)

The issue is more common with Python 3.14 (very new). Consider using Python 3.11 or 3.12.

**Steps in Render:**
1. Add a `runtime.txt` file to your project root
2. Trigger redeploy

---

## What Was Changed

### 1. Fixed `routes/order_routes.py`
Made razorpay import optional so the app can start even if razorpay has issues:

```python
# Try to import razorpay, but don't fail if it's not available
try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False
    razorpay = None
```

### 2. Updated `requirements.txt`
Added setuptools explicitly:
```
setuptools>=65.5.0
```

---

## Verification

After deployment succeeds, verify the app is working:

1. **Check App URL:** Visit `https://your-app.onrender.com`
2. **Check Logs:** Look for any import errors in Render logs
3. **Test API:** Try accessing `/api/products` or `/api/auth/verify`

---

## Current Deployment Status

✅ Routes modules created (auth, product, cart, order, admin, contact, chat, tribute)
✅ Utils modules created (auth decorators, db connection)
✅ Razorpay import made optional
✅ setuptools added to requirements.txt
⏳ Waiting for git push and redeploy

---

## Next Steps

1. **Commit and push changes** (if not done already)
2. **Wait for Render to redeploy** (3-5 minutes)
3. **Check deployment logs** for any errors
4. **Initialize database** if needed: `python init_cloud_db.py`
5. **Test the application**

If deployment still fails, check Option 2 or Option 3 above.
