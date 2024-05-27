export HADOOP_VERSION=3.3.6
export JARS_DIR=conf/jars

curl -L --output $JARS_DIR/mysql-connector-j-8.4.0.jar https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar && \
  curl -L --output $JARS_DIR/aws-java-sdk-bundle-1.12.730.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.730/aws-java-sdk-bundle-1.12.730.jar && \
  curl -L --output $JARS_DIR/hadoop-aws-$HADOOP_VERSION.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-$HADOOP_VERSION.jar
