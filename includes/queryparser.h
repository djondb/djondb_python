// =====================================================================================
// 
//  @file:  queryparser.h
// 
//  @brief:  
// 
//  @version:  1.0
//  @date:     05/23/2015 02:25:21 PM
//  Compiler:  g++
// 
//  @author:  Juan Pablo Crossley (Cross), cross@djondb.com
// 
// This file is part of the djondb project, for license information please refer to the LICENSE file,
// the application and libraries are provided as-is and free of use under the terms explained in the file LICENSE
// Its authors create this application in order to make the world a better place to live, but you should use it on
// your own risks.
// 
// Also, be adviced that, the GPL license force the committers to ensure this application will be free of use, thus
// if you do any modification you will be required to provide it for free unless you use it for personal use (you may 
// charge yourself if you want), bare in mind that you will be required to provide a copy of the license terms that ensures
// this program will be open sourced and all its derivated work will be too.
// =====================================================================================
#ifndef FILTERPARSER2_INCLUDED_H
#define FILTERPARSER2_INCLUDED_H 

#include "list.h"

typedef struct F_XPathExpression {
	char* xpath;
} F_XPathExpression;

const int EXP_CONSTANT = 0;
const int EXP_SIMPLE = 1;
const int EXP_BINARY = 2;

typedef struct F_BinaryExpression {
	struct F_Expression* left;
	char* oper;
	struct F_Expression* right;
} F_BinaryExpression;

const int CONST_INTEGER = 0;
const int CONST_FLOAT = 1;
const int CONST_STRING = 2;
const int CONST_BOOLEAN = 3;
const int CONST_LONG = 4;

struct F_ConstantExpression {
	int constantType; // CONST_*
	void* value;
};

struct F_Expression {
	int type; // EXP_

	void* expression; // ConstantExpression, BinaryExpression, XpathExpression
};

struct Parser {
	int error;
	char* message;
	List* tokens;
	const char* text;
	int len;
	int pos;
	List* expressions;

	F_Expression* root;
};

Parser* parseFilter(const char* text, int len);
void freeParser(Parser* parser);
char* formatParserError(Parser* parser);

#endif /* FILTERPARSER2_INCLUDED_H */
