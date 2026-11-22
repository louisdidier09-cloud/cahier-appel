import pathlib
p = pathlib.Path('android/app/src/main/AndroidManifest.xml')
t = p.read_text()
perms = ['INTERNET', 'ACCESS_NETWORK_STATE', 'ACCESS_FINE_LOCATION', 'ACCESS_COARSE_LOCATION',
         'FOREGROUND_SERVICE', 'FOREGROUND_SERVICE_LOCATION', 'POST_NOTIFICATIONS',
         'WAKE_LOCK', 'VIBRATE']
add = ''.join('    <uses-permission android:name="android.permission.%s" />\n' % x
              for x in perms if 'android.permission.%s"' % x not in t)
add += '    <uses-feature android:name="android.hardware.location.gps" android:required="false" />\n'
t = t.replace('</manifest>', add + '</manifest>')
svc = ('    <service android:name="com.equimaps.capacitor_background_geolocation.BackgroundGeolocationService" '
       'android:enabled="true" android:exported="true" android:foregroundServiceType="location" />\n')
t = t.replace('</application>', svc + '</application>')
p.write_text(t)
print(t)

import shutil, re
try:
    res = pathlib.Path('android/app/src/main/res')
    ic = pathlib.Path('icons')
    if ic.exists():
        shutil.copytree(ic, res, dirs_exist_ok=True)
        for sp in res.glob('drawable*/splash.png'):
            shutil.copyfile(ic / 'splash.png', sp)
    st = res / 'values' / 'styles.xml'
    if st.exists():
        x = st.read_text()
        if 'Theme.SplashScreen' in x and 'windowSplashScreenBackground' not in x:
            x = re.sub(r'(<style name="AppTheme.NoActionBarLaunch"[^>]*>)', r'\1\n        <item name="windowSplashScreenBackground">#0B2119</item>', x, count=1)
        if 'statusBarColor' not in x:
            x = re.sub(r'(<style name="AppTheme.NoActionBar"[^>]*>)', r'\1\n        <item name="android:statusBarColor">#0B2119</item>\n        <item name="android:navigationBarColor">#0B2119</item>', x, count=1)
        st.write_text(x)
except Exception as e:
    print('personnalisation graphique ignoree :', e)
