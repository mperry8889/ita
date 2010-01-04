package chatServer.serverObjects;

import java.net.Socket;

/**
 * Acts as a buffer class between the user and the chat mechanics.  User commands are interpreted (or rejected)
 * in this class, and then the appropriate server actions are taken.
 * 
 * @author matt
 *
 */
public class User {

	Socket s;
	
	public User(Socket s) {
		this.s = s;
	}
	
	
	
	
}
