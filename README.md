service.subtitles.ktuvit
==================

Ktuvit.me subtitle service for Kodi

## Install (this fork, with automatic updates)

1. In Kodi: Settings > File manager > Add source > `https://lioree.github.io/service.subtitles.ktuvit/` (name it e.g. `ktuvit`).
2. Add-ons > Install from zip file > `ktuvit` > `repository.lioree.ktuvit.zip` (enable *Unknown sources* if asked).
3. Add-ons > Install from repository > *Ktuvit (lioree) Repository* > Subtitles > *Ktuvit.me* > Install.

Kodi then offers new versions by itself. The repository files are built by `tools/build_repo.py` and published on the `gh-pages` branch.

## Encrypted password

In order to get the encoded password:

1. Open [ktuvit.me](https://www.ktuvit.me) in the browser
2. Open [developer tools](https://developers.google.com/web/tools/chrome-devtools/open)  (in Windows <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>c</kbd>
)
3. Enter this code in the **console**: 
```javascript
x = { value: 'MY-PASSWORD' };
loginHandler.EncryptPassword({}, x, 'MY@EMAIL.COM');
copy(x.value); // this will copy your encrypted password to your clipboard
console.log(`Now paste it in the addon's settings at the Encrypted password field`)
``` 
![Gujn9Y8vTF](https://user-images.githubusercontent.com/9304194/94992868-897f0100-0595-11eb-8694-0272ae2f19b9.gif)

