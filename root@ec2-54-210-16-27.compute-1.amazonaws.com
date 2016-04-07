{
 "metadata": {
  "name": "",
  "signature": "sha256:ae5a9bf2c1ffc2ea543d87c1aaf84da95942c85ff468534ec61ddb3c60b59166"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import pandas as pd\n",
      "import numpy as np"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 2
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import boto\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 2
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "conn = boto.connect_s3(access_key, secret_access_key)\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "ename": "NameError",
       "evalue": "name 'access_key' is not defined",
       "output_type": "pyerr",
       "traceback": [
        "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m\n\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
        "\u001b[1;32m<ipython-input-3-a5fcc0530852>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m()\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mconn\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mboto\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mconnect_s3\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0maccess_key\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0msecret_access_key\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
        "\u001b[1;31mNameError\u001b[0m: name 'access_key' is not defined"
       ]
      }
     ],
     "prompt_number": 3
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(link)\n",
      "\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "ename": "Exception",
       "evalue": "(\"You must build Spark with Hive. Export 'SPARK_HIVE=true' and run build/sbt assembly\", Py4JJavaError(u'An error occurred while calling None.org.apache.spark.sql.hive.HiveContext.\\n', JavaObject id=o74))",
       "output_type": "pyerr",
       "traceback": [
        "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m\n\u001b[1;31mException\u001b[0m                                 Traceback (most recent call last)",
        "\u001b[1;32m<ipython-input-5-e2133730516e>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m()\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mdf\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0msqlContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mread\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'com.databricks.spark.csv'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0moptions\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mheader\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m'true'\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0minferschema\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m'true'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mlink\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
        "\u001b[1;32m/root/spark/python/pyspark/sql/context.pyc\u001b[0m in \u001b[0;36mread\u001b[1;34m(self)\u001b[0m\n\u001b[0;32m    661\u001b[0m         \u001b[1;33m:\u001b[0m\u001b[1;32mreturn\u001b[0m\u001b[1;33m:\u001b[0m \u001b[1;33m:\u001b[0m\u001b[1;32mclass\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m`\u001b[0m\u001b[0mDataFrameReader\u001b[0m\u001b[1;33m`\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    662\u001b[0m         \"\"\"\n\u001b[1;32m--> 663\u001b[1;33m         \u001b[1;32mreturn\u001b[0m \u001b[0mDataFrameReader\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    664\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    665\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
        "\u001b[1;32m/root/spark/python/pyspark/sql/readwriter.pyc\u001b[0m in \u001b[0;36m__init__\u001b[1;34m(self, sqlContext)\u001b[0m\n\u001b[0;32m     54\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     55\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0m__init__\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0msqlContext\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 56\u001b[1;33m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_jreader\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0msqlContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_ssql_ctx\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mread\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     57\u001b[0m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_sqlContext\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0msqlContext\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     58\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
        "\u001b[1;32m/root/spark/python/pyspark/sql/context.pyc\u001b[0m in \u001b[0;36m_ssql_ctx\u001b[1;34m(self)\u001b[0m\n\u001b[0;32m    689\u001b[0m             raise Exception(\"You must build Spark with Hive. \"\n\u001b[0;32m    690\u001b[0m                             \u001b[1;34m\"Export 'SPARK_HIVE=true' and run \"\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 691\u001b[1;33m                             \"build/sbt assembly\", e)\n\u001b[0m\u001b[0;32m    692\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    693\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0m_get_hive_ctx\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
        "\u001b[1;31mException\u001b[0m: (\"You must build Spark with Hive. Export 'SPARK_HIVE=true' and run build/sbt assembly\", Py4JJavaError(u'An error occurred while calling None.org.apache.spark.sql.hive.HiveContext.\\n', JavaObject id=o74))"
       ]
      }
     ],
     "prompt_number": 5
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import pyspark"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 6
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import pandas as pd\n",
      "import numpy as np\n",
      "from datetime import timedelta\n",
      "from datetime import datetime\n",
      "#import statsmodels.api as sm\n",
      "#from statsmodels import tsa\n",
      "from os import walk\n",
      "from pyspark import SparkContext\n",
      "from pyspark.mllib.classification import LogisticRegressionWithSGD\n",
      "from pyspark.ml import tuning\n",
      "from pyspark.ml import Pipeline\n",
      "from pyspark.mllib.tree import RandomForest, RandomForestModel\n",
      "from pyspark.sql import SQLContext"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "ERROR:py4j.java_gateway:An error occurred while trying to connect to the Java server (127.0.0.1:57902)\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/local/lib/python2.7/site-packages/py4j-0.9.2-py2.7.egg/py4j/java_gateway.py\", line 713, in start\n",
        "    self.socket.connect((self.address, self.port))\n",
        "  File \"/usr/lib64/python2.7/socket.py\", line 228, in meth\n",
        "    return getattr(self._sock,name)(*args)\n",
        "error: [Errno 111] Connection refused\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "ERROR:py4j.java_gateway:An error occurred while trying to connect to the Java server (127.0.0.1:57902)\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/local/lib/python2.7/site-packages/py4j-0.9.2-py2.7.egg/py4j/java_gateway.py\", line 713, in start\n",
        "    self.socket.connect((self.address, self.port))\n",
        "  File \"/usr/lib64/python2.7/socket.py\", line 228, in meth\n",
        "    return getattr(self._sock,name)(*args)\n",
        "error: [Errno 111] Connection refused\n"
       ]
      }
     ],
     "prompt_number": 7
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": []
    }
   ],
   "metadata": {}
  }
 ]
}