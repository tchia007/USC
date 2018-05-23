import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class WordCount {

	//Mapper class
	public static class TokenizerMapper extends Mapper<Object, Text, Text, Text>
	{
		private Text word = new Text();
		private Text docID = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			//getting filename to store as docID 
			String filename = ( (FileSplit) context.getInputSplit()).getPath().getName();
			docID.set(filename.substring(0, filename.length()-4)); //removing the '.txt' portion of the filename

			//parsing document content to output word, docID
			StringTokenizer itr = new StringTokenizer(value.toString().split("\\t")[1]);
			while (itr.hasMoreTokens()) {
				word.set(itr.nextToken());
				context.write(word, docID); 
			}
		}
	}

	//Reducer class
	public static class IntSumReducer extends Reducer<Text,Text,Text,Text> 
	{
		private String docID_count = "";

		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			HashMap<String, Integer> map = new HashMap<String, Integer>();
			for(Text t : values){
				String docID = t.toString();
				if(!map.containsKey(docID)){
					map.put(docID, 1);
				}
				else{
					map.put(docID, map.get(docID) + 1);
				}
			}
			//cleaning the map output 
			docID_count = map.toString().replace("{", "").replace("}","").replace("=",":").replace(",", "").replace(" ", "	");
			context.write(key, new Text(docID_count)); 
		}
	}

	public static void main(String[] args) throws Exception
	{
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "word count");
		job.setJarByClass(WordCount.class);
		job.setMapperClass(TokenizerMapper.class);
		job.setReducerClass(IntSumReducer.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}