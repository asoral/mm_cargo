# Multi Mode Cargo System
## _Manage your Accounts Based Marketing business in ERPNext using all-in-one app._

![image](https://erp.dexciss.com/files/dex_new_logo_black.png)(https://erp.dexciss.com)

[![Build Status](https://app.travis-ci.com/asoral/dsc.svg?token=7se28HZpackz4WYZS3Uv&branch=master)](https://app.travis-ci.com/github/asoral/dsc)

"B2B Marketing" is an ERPNext app to design ABM Campaigns, upload bulk data, maintain data integrity and security. Also, create leads and bill your customers using standard ERPNext invoicing module.

- Automated Calling
- Voice Call recording
- Quality trigger and Procedures
- FTE reporting
- 100% open-source within ERPNext
- ✨Quick and Easy Setup ✨

## Features

- Design ABM Campaigns.
- Bulk upload lead data.
- DNC Managmement.
- Automated Calling Queue management.
- FTE and Agent Quality reports.




> ABM managment tools are meant to hold a lot of contact data and design campaigns based on particular filter of the campaign manager. B2B Marketing app is designed keeping in mind how ABM operates.

## Installation

Using bench, install ERPNext as mentioned on the official frappe documentation.
Once ERPNext is installed, add dsc app to your bench by running
```sh
$ bench get-app https://github.com/asoral/b2b_marketing --branch version-14
$ bench setup requirements
$ bench --site <site-name> install-app b2b_marketing
```
>Note: use the correct branch as your ERPNext installed version asks for.

## Functionality
 
* Design Campaigns using Campaign Designer.
![image](https://user-images.githubusercontent.com/11851156/210568537-6b19b16a-010c-4794-860d-c58134f0a9fb.png)


* Campaigns are created with contacts added from the database using the filters set in the designer.
![image](https://user-images.githubusercontent.com/11851156/210568738-a2c31d51-44ef-407d-b2ba-2b6b560ba944.png)


* Calls are scheduled based on the sequence defined on the campaign and assigned to the pool of agents for equal load balancing in the team.
![image](https://user-images.githubusercontent.com/11851156/210568987-234e451e-435c-4743-9a12-d21e094ac55d.png)


* Calls can be automated using the Call Campaign screen and recording and Quality can be reviewed based on the policied defined on the camoaign designer.
![image](https://user-images.githubusercontent.com/11851156/210569225-3bfedf40-1900-4369-8761-6e52f7a1d9db.png)
![image](https://user-images.githubusercontent.com/11851156/210569322-d4f4015b-fd3f-46cd-8e77-82394614f4ec.png)


### Calling will be charged extra as per your provider. Recording is also available as a feature.


## License
GNU/General Public License (see license.txt as being followed by ERPNext repository)
The dsc App code is licensed as GNU General Public License (v3) and the Documentation is licensed as Creative Commons (CC-BY-SA-3.0) and the copyright is owned by Dexciss Technology Pvt Ltd and Dexciss Technology LLC (Dexciss) and Contributors.

By contributing to dsc, you agree that your contributions will be licensed under its GNU General Public License (v3).

**ERPNext App, Hell Yeah!**
