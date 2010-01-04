package chatServer;
import gnu.getopt.Getopt;

import java.io.IOException;


public class Main {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		
		Getopt optp = new Getopt("ChatServer", args, "t:");
		
		int c;
		while ((c = optp.getopt()) != -1) {
			switch (c) {
				case 't':
					System.out.println("Your arg is " + optp.getOptarg() + "\n");
					break;
				case 'p':
					break;
				case 'v':
					break;
			}
				
				
		}	
		
		Dispatcher cs = new Dispatcher(6667);
		

	}

}
