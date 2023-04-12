# Set the image ID to use for the Docker container
IMG_ID=us-docker.pkg.dev/android-emulator-268719/images/r-google-x64:30.0.23

# Define the initial port numbers
let port1=29998
let port2=29999

# Loop through 3 times
for i in $(seq 1 $var);
do
    # Increment the port numbers for each iteration
    ((port1 += 2))
    ((port2 += 2))

    # Start the Docker container
    docker run -d --rm --privileged -m 8g --memory-reservation=2g \
    -e EMULATOR_ARGS="-no-window -no-boot-anim -netdelay none -no-snapshot \
    -wipe-data -verbose -no-audio -gpu swiftshader_indirect -no-snapshot \
    -read-only -partition-size 512" --device /dev/kvm -p $port1:5554 \
    -p $port2:5555 budtmo/docker-android-x86-8.0:1.8-p1

    # Wait for the container to start up
    sleep 10

    # Connect to the Android emulator
    adb connect localhost:$port2
done
