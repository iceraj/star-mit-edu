#!/bin/bash

# based on https://bugs.launchpad.net/ubuntu/+bug/987182
# didn't fix problem.  Had to change deb source to http://archive.ubuntu.com/ubuntu/
#echo "Acquire::http::Pipeline-Depth \"0\";" > /etc/apt/apt.conf.d/90-fix-s3

# based on instructions from http://ronert-obst.com/blog/2013-09-01-starcluster.html

set -ex

# drop repo which appears to be gone
grep -v www.cs.wisc.edu /etc/apt/sources.list > /tmp/new-sources-list
mv /tmp/new-sources-list /etc/apt/sources.list

# Add CRAN to sources
echo deb http://cran.case.edu/bin/linux/ubuntu precise/ > /etc/apt/sources.list.d/50_cran.list

# Add key used to sign packages
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

apt-get update
apt-get install -y r-base r-base-dev r-recommended joe fish

echo "DONE with Ubuntu package installation on $(hostname -s)."

R --vanilla >/tmp/R-install.log 2>&1 <<EOF

install.packages(c("gbm", "foreach", "doMC", "getopt", "caTools","caret","batch","RJSONIO", "apcluster", "multicore", "doSNOW", "futile.logger", "party", "AUC", "data.table"),   
   repos='http://cran.rstudio.com')

EOF

echo "DONE with R package installation on $(hostname -s)."
