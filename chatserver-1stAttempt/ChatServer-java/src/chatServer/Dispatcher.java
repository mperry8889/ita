package chatServer;

import java.io.IOException;
import java.net.ServerSocket;

public class Dispatcher {

	public Dispatcher(int port) throws IOException {

		System.out.println("starting server");
		
		ServerSocket s = new ServerSocket(port);
		while (true) {
			s.accept();
			s.close();
			break;
		}
		
		System.out.println("server exited");
		
	}
	
}
