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
