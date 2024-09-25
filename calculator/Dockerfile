FROM python:3

ARG ANDROID_API_LEVEL=30
ARG ANDROID_BUILD_TOOLS_LEVEL=33.0.1
ARG EMULATOR_NAME='test'
# ENV APK=$(ls | grep apk)
ARG APK=''

COPY $APK /
COPY testandroidcalculator.py /
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt
# Update apt and instal wget and npm
RUN apt update && apt install -y openjdk-11-jdk wget npm
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64" \
    PATH=$PATH:$JAVA_HOME/bin
# Install appium via npm command
RUN npm i -g appium
# Install Android SDK tools and images for particular API level
ENV SDK_VERSION=commandlinetools-linux-8512546_latest

RUN wget https://dl.google.com/android/repository/${SDK_VERSION}.zip -P /tmp \
&& unzip -d /tmp /tmp/${SDK_VERSION}.zip && rm /tmp/${SDK_VERSION}.zip \
&& mkdir -p /opt/android/cmdline-tools/latest \
&& mv  -v /tmp/cmdline-tools/* /opt/android/cmdline-tools/latest \
&& yes Y | /opt/android/cmdline-tools/latest/bin/sdkmanager --install "platform-tools" "system-images;android-${ANDROID_API_LEVEL};google_apis;x86" "platforms;android-${ANDROID_API_LEVEL}" "build-tools;${ANDROID_BUILD_TOOLS_LEVEL}" "emulator" \
&& yes Y | /opt/android/cmdline-tools/latest/bin/sdkmanager --licenses \
&& echo "no" | /opt/android/cmdline-tools/latest/bin/avdmanager create avd -n "test" -k "system-images;android-${ANDROID_API_LEVEL};google_apis;x86"

ENV ANDROID_HOME=/opt/android
ENV PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$(pwd):$PATH"

ADD start.sh /

RUN chmod +x start.sh
