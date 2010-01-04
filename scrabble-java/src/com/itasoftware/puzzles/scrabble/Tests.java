package com.itasoftware.puzzles.scrabble;

import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.List;

import com.itasoftware.puzzles.scrabble.Scrabble;

import java.io.BufferedReader;
import java.io.StringReader;
import java.util.Arrays;
import org.testng.Assert;

@Test
public class Tests {

	private Character[] EXAMPLE_LETTERS = { 'w', 'g', 'd', 'a', 's', 'x', 'z',
			'c', 'y', 't', 'e', 'i', 'o', 'b' };
	private String[] EXAMPLE_OUTPUT = { "azotised", "bawdiest", "dystocia",
			"geotaxis", "iceboats", "oxidates", "oxyacids", "sweatbox",
			"tideways" };

	@Test()
	public void GivenExample() {
		StringBuilder sb = new StringBuilder();

		for (String str : EXAMPLE_OUTPUT) {
			sb.append(str + "\n");
		}

		StringReader sr = new StringReader(sb.toString());
		BufferedReader br = new BufferedReader(sr);

		List<String> words = Scrabble.scrabble(br, new ArrayList<Character>(Arrays
				.asList(EXAMPLE_LETTERS)));
		Assert.assertEquals(words, new ArrayList<String>(Arrays
				.asList(EXAMPLE_OUTPUT)));
	}

	@Test()
	public void SimpleDuplicates() {
		String[] input = { "aa", "bb" };
		StringBuilder sb = new StringBuilder();
		for (String i : input) {
			sb.append(i + "\n");
		}

		Character[] letters = { 'a', 'a', 'b', 'b' };

		StringReader sr = new StringReader(sb.toString());
		BufferedReader br = new BufferedReader(sr);

		List<String> words = Scrabble.scrabble(br, new ArrayList<Character>(Arrays
				.asList(letters)));
		Assert.assertEquals(words, new ArrayList<String>(Arrays.asList(input)));
	}

	@Test()
	public void NontEnoughLetters() {
		String[] input = { "aa", "bb" };
		StringBuilder sb = new StringBuilder();
		for (String i : input) {
			sb.append(i + "\n");
		}

		Character[] letters = { 'a', 'b' };

		StringReader sr = new StringReader(sb.toString());
		BufferedReader br = new BufferedReader(sr);

		List<String> words = Scrabble.scrabble(br, new ArrayList<Character>(Arrays
				.asList(letters)));
		Assert.assertEquals(words, new ArrayList<String>());
	}
	
	@Test()
	public void WeirdBug() {
		String[] input = { "ethylenediaminetetraacetates" };
		StringBuilder sb = new StringBuilder();
		for (String i : input) {
			sb.append(i + "\n");
		}

		StringReader sr = new StringReader(sb.toString());
		BufferedReader br = new BufferedReader(sr);

		List<String> words = Scrabble.scrabble(br, new ArrayList<Character>(Arrays
				.asList(EXAMPLE_LETTERS)));
		Assert.assertEquals(words, new ArrayList<String>());
		
	}

}
