## Setup AWS Elastic Beanstalk CLI environment  

### 0. Create a conda virtual environment with Python 3.6
`conda create --name py36 python = 3.6`  
Activate the environment:
`activate py36`  

Open a command prompt from Anaconda and use conda/pip to install other packages you might want/need. Also install Flask:   
`conda install requests numpy flask=1.0.2`  
`conda install -c conda-forge rasterio geopandas`  
`pip install mapbox`

Install `virtualenv`   
`conda install virtualenv`   

### 1. Install AWS EB CLI  
See https://github.com/aws/aws-elastic-beanstalk-cli-setup. Note that you must install with a special command in order to get Python 3.6 which is required to run Flask on AWS EB.  

Change to your project directory.  

First, clone the repo:
`git clone https://github.com/aws/aws-elastic-beanstalk-cli-setup.git `  

Then, switch to the folder created by the clone and install EB CLI with Python 3.6 (make sure to change the path to where python 3.6 sits on your computer!):  
`python scripts/ebcli_installer.py --python-installation /path/to/python36/on/your/computer`  


Follow the prompts to add the `eb` command to your Windows path and restart the command prompt window from the py36 environment.  

## Setting up a Flask Server on AWS Elastic Beanstalk  
using: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html  

cd to your project directory (where your application sits)

### 1. Create a virtual environment using virtualenv:  
`python -m virtualenv virt`  
activate it:  
`virt\Scripts\activate`  

### 1. Install Flask in the virtual environment
`pip install flask==1.0.2`  

### 2. Get list of installed package dependencies for use by AWS EB:  
`pip freeze > requirements.txt`  

Now you are in a virtual environment `virt` inside the py36 conda environment. eb cli has been installed.

Check that eb works, type `eb --version` and ensure you get the correct response. You should see  
`(.ebcli-virtual-env)(py36) C:\pathto\your\app>`  

## Setting up an Elastic Beanstalk Application  
Using directions from here: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.html  
Note that this tutorial sets up an example application. I assume here that you already have your AWS account. Make sure you are signed in.

### 1. Create an EB environment and deploy your flask application  
First, create the application named 'flask-tutorial' and configure a local repository to create environments:  
`eb init -p python=3.6 flask-tutorial --region us-west-2`  
Make sure to provide your credentials when prompted.
Create the environment  
`eb create flask-env`

When finished, open website with `eb open`  


## Terminating environment  
Cleanup   
`eb terminate flask-env` or complete in the AWS console for Elastic Beanstalk.
