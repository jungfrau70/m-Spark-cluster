
from pyspark import SparkContext, SparkConf
conf = (SparkConf().setMaster("spark://master:7077")
    .set("spark.executor.cores", "1")
    .set("spark.cores.max", "2")
    .set('spark.executor.memory', '1g')
)

sc = SparkContext(conf=conf)

logFilepath = "hdfs://master:9000/wordcount.txt"  
logData = sc.textFile(logFilepath).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
