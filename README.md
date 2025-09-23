# AppBuddy: Learning to Accomplish Tasks in Mobile Apps via Reinforcement Learning
Human beings, even small children, quickly become adept at figuring out how to use applications on their mobile devices. Learning to use a new app is often achieved via trial-and-error, accelerated by transfer of knowledge from past experiences with like apps. The prospect of building a smarter smartphone --- one that can learn how to achieve tasks using mobile apps --- is tantalizing. In this paper we explore the use of Reinforcement Learning (RL) with the goal of advancing this aspiration. We introduce AppBuddy, an RL-based framework for learning to accomplish tasks in mobile apps. RL agents are provided with states derived from the underlying representation of on-screen elements, and rewards that are based on progress made in the task. Agents can interact with screen elements by tapping or typing. Our experimental results, over a number of mobile apps, show that RL agents can learn to accomplish multi-step tasks, as well as achieve modest generalization across different apps. We develop a platform which addresses several engineering challenges to enable an effective RL training environment. The platform includes a suite of mobile apps and benchmark tasks that supports a diversity of RL research in the mobile app setting. A video demonstration of the system is available here: https://youtu.be/n7E7CZDYZM0.

Implementation of AppBuddy: Learning to Accomplish Tasks in Mobile Appsvia Reinforcement Learning, Canadian AI 2021. 

## Prerequisites
Create a conda environment with prerequisite packages
```
conda create --name <env> --file req_conda.txt
```

Install adb
```
sudo apt-get install android-tools-adb android-tools-fastboot
```

Initialize the adb server and ensure that there is a device runnning

```
adb devices
```

## Launch emulators

The script is start_emulators.sh under the scripts folder. The number of emulators launched by the script can be changed by modifying the var variable. It is 35 by default.
```
sh start_emulators.sh
```
Using 
```
adb devices
```
you can check whether the emulators have been properly initialized

## Start Bert Services
Clone this repo - https://github.com/hanxiao/bert-as-service and download the bert model (uncased_L-12_H-768_A-12) in the repo. After that, Run the following command to start the bert service. 

```
nohup bert-serving-start -model_dir uncased_L-12_H-768_A-12 -num_worker=20 -port 5000 -port_out 5005 &
```

## How to run the code - OpenAI baselines

Install baselines
```
cd baselines
```
Then run
```
pip install -e .
```
Then run
```
cd ../app_buddy/android_gym
```
and run

```
pip install -e .
```
and then 
```
cd ../..
```
Then download the F-Droid apps' APKs
```
wget https://f-droid.org/repo/org.openintents.shopping_100221.apk
wget https://f-droid.org/repo/com.nishantboro.splititeasy_1.apk
wget https://f-droid.org/repo/com.angrydoughnuts.android.alarmclock_15.apk
```
Install the F-Droid apps using the downloaded APKs (xxxxx should be replaced with the emulator port (e.g., 30001) which can be found when executing adb devices)
```
adb -s localhost:xxxxx install com.angrydoughnuts.android.alarmclock_15.apk
adb -s localhost:xxxxx install com.nishantboro.splititeasy_1.apk
adb -s localhost:xxxxx install org.openintents.shopping_100221.apk
```

To choose what task to run (settings, shopping, alarm, or split), set one of the variables in lines 53-56 in android_gym⁩/gym_android⁩/⁨envs/android_env.py⁩ to 1. To choose the difficulty (easy, medium, or hard), uncomment one of the lines in lines 58-60 in the same file.

Finally, run

```
OPENAI_LOGDIR=$HOME/logs OPENAI_LOG_FORMAT=csv python3 -m baselines.run --alg=ppo2 --env=Android-v0 --network=mlp --num_timesteps=4e6 --log_interval=1
```
## Train the agent on a new app

To train an agent on a new app (i.e., not one of the four included apps: split, shopping, alarm, and settings), we must implement two app-specific functions: reset and get_reward.

In the function restart_env in android_env.py, you will find calls to the four app-specific reset functions that are currently implemented. Let's say you have an app called FooApp. To experiment with this app, you need to write a function that resets the app. For inspiration, take a look at the restart_settings function in settings_app.py. There, adb commands are issued to clear the app's data and to reopen the app since the clear command causes the app to terminate.

Second, you will need to implement a get_reward function that, given the current state of the emulator, returns a numerical reward as well as whether or not the episode is done (in case the task has been achieved). In android_env.py, within the step() function, there are four calls to the four app-specific get_reward functions. For FooApp, you should add a call to the FooApp-specific get_reward function that you will create.

Once again, we can look at settings_app.py for inspiration. The function get_reward_settings_app accepts as input the state of the emulator (i.e., the parsed view hierarchy) and returns the value of the reward as well as whether or not the episode is done. 

## Contributors
Maayan Shvo (maayanshvo@cs.toronto.edu) \
Zhiming Hu (zhiming.hu@samsung.com) \
Rodrigo	Toro Icarte (rntoro@cs.toronto.edu)\
Iqbal Mohomed (i.mohomed@samsung.com)\
Allan	Jepson (allan.jepson@samsung.com)\
Sheila A.	McIlraith	(sheila@cs.toronto.edu)

