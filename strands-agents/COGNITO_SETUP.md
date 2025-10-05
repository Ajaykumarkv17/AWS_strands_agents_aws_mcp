# AWS Cognito Setup Guide

## Step 1: Create Cognito User Pool

1. Go to AWS Console → Amazon Cognito
2. Click "Create user pool"
3. **Configure sign-in experience:**
   - Provider types: "Cognito user pool"
   - Cognito user pool sign-in options: Check "Email"
   - Click "Next"

4. **Configure security requirements:**
   - Password policy: Choose "Cognito defaults" or customize
   - Multi-factor authentication: "No MFA" (or enable if needed)
   - Click "Next"

5. **Configure sign-up experience:**
   - Self-registration: "Enable self-registration"
   - Required attributes: Select "email"
   - Click "Next"

6. **Configure message delivery:**
   - Email provider: "Send email with Cognito"
   - Click "Next"

7. **Integrate your app:**
   - User pool name: `memory-agent-pool`
   - Hosted authentication pages: Check "Use the Cognito Hosted UI"
   - Domain: Choose "Use a Cognito domain"
   - Cognito domain: `memory-agent-{random}` (must be unique)
   - Initial app client:
     - App client name: `memory-agent-client`
     - Client secret: "Generate a client secret"
     - Allowed callback URLs: `http://localhost:8501,https://your-amplify-domain.com`
     - Allowed sign-out URLs: `http://localhost:8501,https://your-amplify-domain.com`
     - OAuth 2.0 grant types: Check "Authorization code grant"
     - OpenID Connect scopes: Check "OpenID", "Email", "Profile"
   - Click "Next"

8. **Review and create:**
   - Review settings
   - Click "Create user pool"

## Step 2: Get Configuration Values

After creation, note these values:

1. **User Pool ID**: Found on pool overview page
   - Format: `us-east-1_xxxxxxxxx`

2. **App Client ID**: Go to "App integration" tab → "App clients"
   - Copy "Client ID"

3. **App Client Secret**: In app client details
   - Click "Show client secret"
   - Copy the secret

4. **Cognito Domain**: In "App integration" tab
   - Format: `https://memory-agent-{random}.auth.us-east-1.amazoncognito.com`

## Step 3: Configure Environment Variables

Create `.env` file:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Cognito OAuth2
COGNITO_DOMAIN=https://memory-agent-{random}.auth.us-east-1.amazoncognito.com
COGNITO_CLIENT_ID=your_client_id
COGNITO_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8501

# API
API_BASE_URL=http://localhost:8000
```

## Step 4: Create Test User

1. Go to your User Pool → "Users" tab
2. Click "Create user"
3. Fill in:
   - Email: `test@example.com`
   - Temporary password: Create one
   - Uncheck "Send an email invitation"
4. Click "Create user"

## Step 5: Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run API
python run.py

# In another terminal, run Streamlit
streamlit run streamlit_auth.py
```

## Step 6: AWS Amplify Deployment

1. **Update callback URLs** in Cognito:
   - Add your Amplify domain: `https://your-app.amplifyapp.com`

2. **Set environment variables** in Amplify Console:
   - Go to App Settings → Environment variables
   - Add all variables from `.env`

3. **Deploy:**
   - Connect GitHub repository
   - Amplify will use `amplify.yml` for build

## Troubleshooting

**Error: "redirect_uri_mismatch"**
- Ensure callback URL in Cognito matches exactly (including http/https)

**Error: "invalid_client"**
- Check CLIENT_ID and CLIENT_SECRET are correct

**Token not appearing:**
- Check browser console for errors
- Ensure popup blockers are disabled

## Security Notes

- Never commit `.env` file
- Use HTTPS in production
- Enable MFA for production users
- Rotate client secrets regularly
