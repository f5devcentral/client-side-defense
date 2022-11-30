# F5® Distributed Cloud Platform Client-Side Defense (F5 XC CSD) Automation
---
**Table of Contents:** <br />
---
&nbsp;&nbsp;&nbsp;&nbsp;•	**[Overview](#overview)** <br />
&nbsp;&nbsp;&nbsp;&nbsp;•	**[Deployment design](#deployment-design)** <br />
&nbsp;&nbsp;&nbsp;&nbsp;•	**[Prerequisites](#prerequisites)** <br />
&nbsp;&nbsp;&nbsp;&nbsp;•	**[Steps to run the workflow](#steps-to-run-the-workflow)** <br />
&nbsp;&nbsp;&nbsp;&nbsp;•	**[Sample output logs](#sample-output-logs)** <br />
<br />

**Overview:**<br />
---
F5® Distributed Cloud Platform Client-Side Defense (F5 XC CSD) feature provides a multi-phase protection system that protects web applications against Magecart-style and other malicious JavaScript attacks. This multi-phase protection system includes detection, alerting, and mitigation. <br />

&nbsp;&nbsp;&nbsp;&nbsp;• `Detection`: A continuously evolving signal set allows CSD to understand when scripts on web pages exhibit signs of exfiltration. CSD detects                            network requests made by malicious scripts that attempt to exfiltrate PII data. <br />
&nbsp;&nbsp;&nbsp;&nbsp;• `Alerting`: CSD generates timely alerts on the behavior of malicious scripts, provided by a continuously improving Analysis Engine. The                                  Analysis Engine contains a machine learning component for accurate and informative analysis and provides details on the behavior of                                    malicious script to help troubleshoot and identify the root cause. <br />
&nbsp;&nbsp;&nbsp;&nbsp;• `Mitigation`: CSD detects threats in real-time and provides enforcement with one-click mitigation. CSD leverages the same obfuscation and                                signal technology as F5® Distributed Cloud Bot Defense, delivering unparalleled efficacy. <br />

![1](https://docs.cloud.f5.com/docs/static/3491464ceb02f6a3c83c64944b1b62db/dc5ab/csd-data-flow-new.png) <br />
<br />

**Deployment design:**<br />
---
Article reference: https://community.f5.com/t5/technical-articles/javascript-supply-chains-magecart-and-f5-xc-client-side-defense/ta-p/296612 <br />

The objective of this automation is to deploy and test basic `Client-Side-Defense` feature using `Terraform` and `Python` by implementing below steps: <br />
1.	Deploy a demo application in AWS which hosts a simple web login page which captures provided username and passwords and sends these details to a 3rd party malicious domain control server `c2-server.f5cloudbuilder.dev`. Check `application-code.html` file in application folder for more details.)<br />
2.	Deploy origin pool and load balancer in F5 XC using above created backend server public IP <br />
3.	Generate traffic by trying to login to web page using selenium UI automation <br />
4.	Validate if malicious domain network transaction is getting detected in `Client Side Defense` dashboard <br />

`Note: Currently this repo covers malicious domain and fields detection only and mitigation part will be published in future articles.` <br />

![image](https://user-images.githubusercontent.com/6093830/199646117-2f8b2f65-cf36-4be4-8740-41c09d2531e8.png) <br />
<br />

**Prerequisites:**<br />
---
1.	F5 Distributed Cloud account. Refer https://console.ves.volterra.io/signup/start for account creation <br />
2.	Create a F5 XC API Certificate and APIToken. Please see this page for generation: [https://docs.cloud.f5.com/docs/how-to/user-mgmt/credentials](https://docs.cloud.f5.com/docs/how-to/user-mgmt/credentials) <br />
3.	Extract the certificate and the key from the .p12: <br />
```
    openssl pkcs12 -info -in certificate.p12 -out private_key.key -nodes -nocerts
    openssl pkcs12 -info -in certificate.p12 -out certificate.cert -nokeys
```
4.	Move the cert and key files to the repository root folder <br />
5.	Create and replace EC2 instance private and pub files to `application` folder with names `aws-key.pem` and `aws-key.pub`  <br />
6.	Create a namespace in F5 XC console with name `automation-apisec` <br />
7.	Make sure to delegate domain in F5 XC console. Please follow the steps mentioned in doc: [https://docs.cloud.f5.com/docs/how-to/app-networking/domain-delegation](https://docs.cloud.f5.com/docs/how-to/app-networking/domain-delegation) <br />
8.	AWS Account with `Access key` and `Secret key` (if in organisation then need session token). Refer https://aws.amazon.com/resources/create-account/ for account creation <br />
9.  Protected domain is already onboarded in F5 XC Client Side Defense configuration. Refer: https://docs.cloud.f5.com/docs/how-to/advanced-security/csd#add-a-domain-for-csd-protection for more details
<br />


**Steps to run the workflow:**<br />
---
1.	In repo `Settings`, navigate to secrets, then expand `Actions` and update your AWS credentials aquired from Prerequisites-step-8. 
    If they are not available please create them with names `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` and `AWS_SESSION_TOKEN` <br />
    > Note: If session token is not needed then lines 41 and 115 have to be removed from workflow file: `client-side-defense.yml` as they belong to session token
2.	Check the `variables.tf` and update `api_url` and `domain` fields as per your tenant and needed LB domain name <br />
3.	Open `test_csd.py` file and update your `APIToken` aquired from Prerequisite-step-2, tenant name and other fields in this file <br />
4.	Navigate to `Actions` tab in the repository and select the workflow to execute <br />
    1. For full end to end testing we have to use `client-side-defense` workflow (this also destroys infra)
    2. For demo purposes and to deploy infra use `Deploy Infra` job flow <br />
      `Note: We have to delete resources manually for this job if not needed.`
    3. You can also execute `CSD Testing` flow if infra is already available and want to run testing validation
5.	Click on `Run workflow` drop-down on the right side of the UI <br />
6.	Select the `main` branch and click `Run workflow` button <br />
7.	Check and expand each job logs to understand script execution <br />
<br />

**Jobs in the workflow:**<br />
---
&nbsp;&nbsp;&nbsp;&nbsp;• `Deploy ` - Deploys demo application in AWS and also origin pool and load balancer in F5 XC console <br />
&nbsp;&nbsp;&nbsp;&nbsp;• `Testing` - Adds domain to CSD feature and validates CSD fields after sending some traffic using selenium <br />
&nbsp;&nbsp;&nbsp;&nbsp;• `Destroy` - Destroys both application and resources created in cloud and F5 XC <br />
<br />

**Sample output logs:**<br />
---
Demo App web page:<br />
![image](https://user-images.githubusercontent.com/6093830/203243279-6bae2d43-9753-499c-a18a-8ef5be9fe088.png) <br />
<br />
Full work-flow output:<br />
![image](https://user-images.githubusercontent.com/6093830/200125265-6417c278-1993-4d3e-abe9-7d6a015db209.png) <br />
<br />
Deployment Job Output: <br />
![image](https://user-images.githubusercontent.com/6093830/200125164-297a815e-8f2f-4da3-87ff-8021529afd45.png) <br />
<br />
Testing Job output: <br />
![image](https://user-images.githubusercontent.com/6093830/200125185-0ce612cc-a196-4e15-8948-d7766d7b70bc.png)
<br />
Destroy Job Output: <br />
![image](https://user-images.githubusercontent.com/6093830/200125237-a21a0c2d-0804-4508-a9b3-4086550ed3c6.png) <br />
<br />

*Some of the issues and debugging steps:*<br />
1. If unable to create LB, Origin pool or WAF in F5 XC check if your cert and key are valid  <br />
2. If terraform is unable to deploy application check if AWS Credentials provided in secrets are working and uptodate  <br />
3. If your HTTPs load balancer status is not coming up as `VIRTUAL_HOST_READY` and app is not accessible please make sure you don't run automation multiple times  <br />
