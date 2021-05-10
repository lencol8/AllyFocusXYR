# ALLY FOCUS

## Certbot renewal SSL
```
certbot -i nginx \
         --dns-digitalocean \
         --dns-digitalocean-credentials /root/.secrets/certbot/digitalocean.ini \
         -d allyfocus.com -d *.allyfocus.com
```

## Create a content index
```
$ mongo
> use allyfocus
> db.content.createIndex( { title: "text", text: "text" } )
```
## Firebase setup
https://console.firebase.google.com/

1. Create **Firestore** DB
**Database -> Create**

2. Enable sing in method (Email and Password)
**Authentication -> Providers**

3. Create user and copy unique identifier of the user (uid)
**Authentication -> Users**

4. Replace ADMIN-USER-ID to your uid
**Database -> Firestore -> Rules**

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth.uid == 'ADMIN-USER-ID';
    }
    match /{document=**} {
      allow read: if true;
    }
  }
}
```
5. Go to Firebase -> **General Settings** (**Gear icon**)
6. Scroll down **-> Firebase SDK snippet -> SDK**
7. Copy **firebaseConfig**
8. Replace **firebaseConfig** in project/src/main.js

## API providers setup
### Plugin for admin chat
1. Create account
https://www.tidio.com/en/?ref=up
2. Replace **appKey** into project/src/main.js to your own

```
Vue.use(VueTidio, { appKey: 'bi5f5nf5eqeokixppy6mysx9ffzwg8ll' });
```

### Etherscan
1. Create Etherscan API keys (3 total)
https://etherscan.io/myapikey
2. Put **etherscanApiKeys** into **project/src/store/index.js**
```
etherscanApiKeys: [
  'API-KEY-1',
  'API-KEY-2',
  'API-KEY-3'
],
```
3. Replace **tokenAddress** into **project/src/store/index.js**

```
tokenAddress: 'TOKEN-ADDRESS'
```

4. Replace **contractABI** into **project/src/store/index.js**

```
contractABI: []
```

### Infura
1. Create Infura Project
https://infura.io/
2. Replace to your provider URL into **project/src/store/index.js** (for production use mainnet instead of ropsten)
```
infuraURL: '',
```

## Project setup

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compile for production
```
npm run build
cd dist
firebase login
firebase init
```
1. Select -> Hosting
2. Select Existing Project
3. What do you want to use as your public directory? **.**
4. Configure as a single-page app (rewrite all urls to /index.html)? **Yes**
5. File ./index.html already exists. Overwrite? **No**
```
firebase deploy
```
