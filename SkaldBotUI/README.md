# SkaldBotUI


## TO RUN DEVELOPMENT

First you may need to have node.js installed on your machine.
Next, I recommend creating a bat file to run the SkaldBotAPI through cmd so you can have the webapi running while testing the UI. This is needed for many UI functions

Then run the following commands through your command window:

* npm install -g @vue/cli **(only need to do this once)**
* npm install -g @vue/cli-service **(only need to do this once)**
* Point to the directory of the SkaldbotUI project
* npm run serve

*If these steps do not work, reach out to me and I will see if I can help.*

## TO RUN PRODUCTION

* npm install -g serve **(only need to do this once)**
* **(Confirm you have the two packages installed in the TO RUN DEVELOPMENT section)**
* Point directory to the SkalbotUI project
* npm run build

**When build finishes**

serve -s {Path to SkaldbotUI}\dist
