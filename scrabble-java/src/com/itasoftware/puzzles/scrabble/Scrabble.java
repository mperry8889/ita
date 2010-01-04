package com.itasoftware.puzzles.scrabble;

import java.util.List;
import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.HashMap;
import java.lang.Character;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.FileReader;
import java.lang.System;

public class Scrabble {

	protected static boolean intersect(String line, List<Character> letters) {

		HashSet<Character> combined = new HashSet<Character>();
		
		/*
		 * Count the number of occurrences of each letter in the line
		 */
		HashMap<Character, Integer> lineMap = new HashMap<Character, Integer>();
		for (Character letter : line.toCharArray()) {
			combined.add(letter);
			if (lineMap.containsKey(letter)) {
				lineMap.put(letter, (Integer) lineMap.get(letter) + 1);
			} else {
				lineMap.put(letter, 1);
			}
		}

		/*
		 * Count the number of occurrences of each letter in the given
		 * array of usable letters
		 */
		HashMap<Character, Integer> letterMap = new HashMap<Character, Integer>();
		for (Character letter : letters) {
			combined.add(letter);
			if (letterMap.containsKey(letter)) {
				letterMap.put(letter, (Integer) letterMap.get(letter) + 1);
			} else {
				letterMap.put(letter, 1);
			}
		}
		
		
		/*
		 * Decide if the line can be spelled with the given letters.
		 *   1. each letter in the line must be in the letters
		 *   2. the letter map must have more occurrences of each letter than
		 *      the line map
		 */
		for (Character letter : combined) {
			
			// letters has the letter, line does not: skip
			if (letterMap.containsKey(letter) &&
					!lineMap.containsKey(letter)) {
				continue;
			}
			
			// line has the letter, letters does not: reject
			if (lineMap.containsKey(letter) &&
				   !letterMap.containsKey(letter)) {
				return false;
			}
			
			// if line map count > letter map count: reject
			Integer lineMapCount = lineMap.get(letter);
			Integer letterMapCount = letterMap.get(letter);
			if (lineMapCount > letterMapCount) {
				return false;
			}
			
		}
		
		return true;
		
	}
	
	public static List<String> scrabble(BufferedReader input, 
			                            List<Character> letters) {
		
		ArrayList<String> accepted = new ArrayList<String>();
		
		// check which lines intersect with the given letters
		String line;
		try {
			while ((line = input.readLine()) != null) {
				line = line.trim();
				if (intersect(line, letters)) {
					accepted.add(line);
				}
			}
		}
		catch (IOException e) {
			return null;
		}
			
		// only return the letters of maximal length
		Integer max_len = 0;
		for (String i : accepted) {
			if (i.length() > max_len) {
				max_len = i.length();
			}
		}
		
		// filter the list by length; this whole procedure is not 
		// incredibly efficient
		ArrayList<String> result = new ArrayList<String>();
		for (String i : accepted) {
			if (i.length() == max_len) {
				result.add(i);
			}
		}
		
		return result;
	}
	

	public static void main(String[] args) {

		// handle command-line arguments; do no error checking
		// or anything fancy		
		FileReader fr;
		try {
			fr = new FileReader(args[0]);
		} catch (FileNotFoundException e) {
			System.out.println("File not found");
			return;
		}
		BufferedReader br = new BufferedReader(fr);
		
		ArrayList<Character> letters = new ArrayList<Character>();
		for (int i = 1; i < args.length; i++) {
			letters.add(args[i].charAt(0));
		}
		
		for (String s : scrabble(br, letters)) {
			System.out.println(s);
		}
		
	}

}
