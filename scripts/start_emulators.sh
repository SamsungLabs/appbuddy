var=35
#IMG_ID=us-docker.pkg.dev/android-emulator-268719/images/r-google-x64:30.0.23
let port1=29998
let port2=29999
for i in $(seq 1 $var);
do
((port1 +=  2))
((port2 +=  2))
#docker run -e "ADBKEY=$(cat ~/.android/adbkey)"  --device /dev/kvm --privileged --publish $port2:5556/tcp --publish $port1:5555/tcp ${IMG_ID} &
docker run --rm --privileged -m 8g --memory-reservation=2g -e EMULATOR_ARGS="-no-window -no-boot-anim -netdelay none -no-snapshot -wipe-data -verbose -no-audio -gpu swiftshader_indirect -no-snapshot -read-only -partition-size 512" --device /dev/kvm -p $port1:5554 -p $port2:5555 budtmo/docker-android-x86-8.0:1.8-p1
sleep 10
adb connect localhost:$port2
done
