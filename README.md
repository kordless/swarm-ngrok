## Ngrok'n Giant Swarm

This repository contains code and information which will allow you to deploy a static HTML site to [Giant Swarm](https://giantswarm.io/) and then serve the content off an [Ngrok](https://ngrok.com/) URL.  Here's what this looks like from a high level:

![Fancy diagram.](https://raw.githubusercontent.com/kordless/swarm-ngrok/master/assets/mockup.png)

### Prerequisites	

#### Giant Swarm
You will need a Giant Swarm account. You can signup for Giant Swarm on their [website](https://giantswarm.io/).  You will also need to install the Giant Swarm command line client:

   	brew tap giantswarm/swarm
	brew install swarm-client

If you aren't using OSX, [check out the instructions](http://docs.giantswarm.io/reference/installation/) for installing on other platforms.

Once you get *swarm* (not to be confused with Docker's [swarm tool](https://github.com/docker/swarm/)) installed, you can authenticate the client with Giant Swarm's service:

	superman:~ kord$ swarm login
	Username or email: kordless@stackgeek.com
	Password:
	Login Succeeded
	Environment kord/dev has been selected
	superman:~ kord$
    
Once you are logged in, you should be able to get your swarm username:

    superman:~ kord$ swarm info
	Cluster status:      reachable
	Swarm CLI version:   0.12.0 (outdated)
	Logged in as user:   kord
	Current environment: kord/dev

If your client is out-of-date, simply update it:

	superman:~ kord$ brew update
	superman:~ kord$ brew upgrade swarm-client
	==> Upgrading 1 outdated package, with result:
	swarm-client 0.13.0
	==> Upgrading swarm-client
	==> Downloading http://downloads.giantswarm.io/swarm/clients/0.13.0/swarm-0.13.0-	darwin-amd64.tar.gz
	######################################################################## 100.0%
	🍺  /usr/local/Cellar/swarm-client/0.13.0: 2 files, 7.3M, built in 4 seconds

Checking again:

	superman:~ kord$ swarm info
	Cluster status:      reachable
	Swarm CLI version:   0.13.0
	Logged in as user:   kord
	Current environment: kord/dev

#### Docker + Boot2Docker
You will need Docker and Boot2Docker installed before you can use the *swarm* command. A [guide is available](https://docs.docker.com/installation/mac/) for installing Boot2Docker on Docker's site.

Once you've got it installed, you'll need to start the instance and source the environment variables:

	$ boot2docker init
	$ boot2docker start
	$ $(boot2docker shellinit)

I'm still not 100% certain how to get the networking stuff configured correctly for accessing the containers when you launch them locally with boot2docker.  I'll try to get a guide out on that soon!

### Video Walkthrough
Here's a quick and dirty walkthough of launching the project on Giant Swarm. As usual, I talk a lot.

[![](https://raw.githubusercontent.com/kordless/swarm-ngrok/master/assets/video.png)](https://vimeo.com/119916590)

### Checkout and Launch

You can checkout the code by doing the following:

    git clone https://github.com/kordless/swarm-ngrok.git

Change into the directory:

	cd swarm-ngrok

There's nothing left to do but push that shizzle:

    make swarm-up

Once that completes, you'll need to find the URL for Ngrok:

	cd docker-ngrok
    swarm logs <instance-id-for-ngrok-component> | grep established
 
Remember, you can ask *swarm* for info on running services as long as you are in the directory that has a *swarm.json* file in it:

	superman:docker-ngrok kord$ swarm status
	App ngrok is up

	service  component        image                                     instanceid     created              status
	ngrok    flask            registry.giantswarm.io/kord/flask-static  02e8e5dd-xxx   2015-02-18 01:57:29  up
	ngrok    ngrok-component  registry.giantswarm.io/kord/ngrok         84be32f9-xxx   2015-02-18 01:57:29  up

***Note: This example has some content truncated for better viewing.***

Here is an example of logs with the URL in them:

	superman:docker-ngrok kord$ swarm logs 84be32f9-dd58-4bb9-afb5-bcf23f54c303 |grep established
	2015-02-18 01:58:26.309237 [INFO] [client] Tunnel established at http://785fb064.ngrok.com
	2015-02-18 01:58:26.310728 [INFO] [client] Tunnel established at https://785fb064.ngrok.com
	
***Note: This example has some content truncated for better viewing.***

### Environment Variables

The Giant Swarm software uses environment variables named after the service directives in your **swarm.json** file.  Those variables are made available inside the containers.  Here's an example of how that works inside the shell script for starting Ngrok:

	$FLASK_PORT_5000_TCP_ADDR
	$FLASK_PORT_5000_TCP_PORT

Those variables are being built off the JSON from the configuration file:

```
{
  "app_name": "ngrok",
  "services": [
    {
      "service_name": "ngrok",
      "components": [
        {
          "component_name": "ngrok-component",
          "image": "registry.giantswarm.io/$username/ngrok",
          "ports": [4040],
          "dependencies": [
            {
              "name": "flask",
              "port": 5000
            }
          ]
        },
        {
          "component_name": "flask",
          "image": "registry.giantswarm.io/$username/flask-static",
          "ports": ["5000/tcp"]
        }
      ]
    }
  ]
}
```

If you have any questions or get stuck, be sure to email me at **kordless at stackgeek dot com**!

