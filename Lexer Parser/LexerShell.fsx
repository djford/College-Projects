// Lexer Shell
// 2/23/2015
// Toby Dragon
// Modified by Daniel Ford
// 4/2/2015

//All tokens from grammar
type Token = 
    |INT_LIT
    |IDENT
    //keywords
    |BOOL_LIT|IF|ELIF|ELSE
    //symbols
    |OPEN_BRACKET|CLOSED_BRACKET
    |OPEN_PAREN|CLOSED_PAREN
    |COMP_OP|MATH_COMP_OP|AO_OP|AS_OP|MD_OP|ASSN_OP
    |NOT_OP
    |NEWLINE
    //anything not recognized as part of the language
    |ERROR
    |EMPTY

type ParseNode =
    |Nonterminal of string * ParseNode list
    |Terminal of Token * string




let rec treeToString node indStr =
    match node with
    |Terminal(token, lexStr) -> indStr + sprintf "%A" token + lexStr
    |Nonterminal(name, parseNodes) -> indStr + name + "\n" + (childrenToString parseNodes (indStr + "\t"))

and childrenToString children indStr =
    match children with
    |[] -> "" 
    |head::[] -> (treeToString head indStr) + "\n"
    |head::tail -> (treeToString head indStr) + "\n" + (childrenToString tail indStr)

            
    
let var toklexList =
    match toklexList with
    |[] -> failwith "Expected var got empty list"
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            | INT_LIT | IDENT | BOOL_LIT -> 
                Nonterminal("<var>", [Terminal(token, lexeme)]), tail
            | NOT_OP ->
                let notNode = Terminal(token, lexeme)
                match tail with
                |[] -> failwith "Empty list"
                |head2::tail2 ->
                    match head2 with
                    |token2,lexeme2 ->
                        match token2 with
                        | INT_LIT | IDENT | BOOL_LIT -> 
                            Nonterminal("<var>", [notNode; Terminal(token2, lexeme2)]), tail
                        |_ -> failwith ("Expected INT_LIT, IDENT, or BOOL_LIT got" + sprintf "%A" token2)
            |_ -> failwith ("Expected INT_LIT, IDENT, BOOL_LIT, or NOT_OP got" + sprintf "%A" token )
                
       


let rec md_exp_rest toklexList =
    match toklexList with
    |[] -> 
        Nonterminal("<md_exp_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |MD_OP -> 
                let mdNode = Terminal(token, lexeme)
                let varNode, listRest1 = var tail
                let restNode, listRest2 = md_exp_rest listRest1
                Nonterminal("<md_exp_rest>", [mdNode; varNode; restNode]), listRest2
            |_ -> 
                Nonterminal("<md_exp_rest", [Terminal(EMPTY, "empty")]), toklexList
        

let md_exp toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        let varNode, listRest1 = var toklexList
        let mdExpRestNode, listRest2 = md_exp_rest listRest1
        Nonterminal("<md_exp>", [varNode; mdExpRestNode]), listRest2
        
let rec math_exp_rest toklexList =
    match toklexList with
    |[] -> 
        Nonterminal("<math_exp_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |AS_OP ->
                let asNode = Terminal(token, lexeme)
                let mdExpNode, listRest1 = md_exp tail
                let restNode, listRest2 = math_exp_rest listRest1
                Nonterminal("<math_exp_rest>", [asNode; mdExpNode; restNode]), listRest2
            |_ ->
                Nonterminal("<math_exp_rest", [Terminal(EMPTY, "empty")]), toklexList
                    
let math_exp toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        let mdNode, listRest1 = md_exp toklexList
        let mathExpRestNode, listRest2 = math_exp_rest listRest1
        Nonterminal("<math_exp>", [mdNode; mathExpRestNode]), listRest2

let rec ao_exp_rest toklexList =
    match toklexList with
    |[] -> 
        Nonterminal("<ao_exp_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |AO_OP ->
                let aoNode = Terminal(token, lexeme)
                let mathExpNode, listRest1 = math_exp tail
                let restNode, listRest2 = ao_exp_rest listRest1
                Nonterminal("<ao_exp_rest>", [aoNode; mathExpNode; restNode]), listRest2
            |_ ->
                Nonterminal("<ao_exp_rest", [Terminal(EMPTY, "empty")]), toklexList

let ao_exp toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        let mathExpNode, listRest1 = math_exp toklexList
        let aoExpRestNode, listRest2 = ao_exp_rest listRest1
        Nonterminal("<ao_exp>", [mathExpNode; aoExpRestNode]), listRest2

let rec exp_rest toklexList =
    match toklexList with
    |[] -> 
        Nonterminal("<exp_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |COMP_OP ->
                let compNode = Terminal(token, lexeme)
                let aoExpNode, listRest1 = ao_exp tail
                let restNode, listRest2 = exp_rest listRest1
                Nonterminal("<exp_rest>", [compNode; aoExpNode; restNode]), listRest2
            |_ ->
                Nonterminal("<exp_rest", [Terminal(EMPTY, "empty")]), toklexList

let exp toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        let aoExpNode, listRest1 = ao_exp toklexList
        let expRestNode, listRest2 = exp_rest listRest1
        Nonterminal("<exp>", [aoExpNode; expRestNode]), listRest2

let rec assn_stmt toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |IDENT ->
                let identNode = Terminal(token, lexeme)
                match tail with
                |[] -> failwith "Empty list"
                |head2::tail2 ->
                    match head2 with
                    |token2,lexeme2 ->
                        match token2 with
                        |ASSN_OP ->
                            let assnNode = Terminal(token2, lexeme2) 
                            let expNode, listRest = exp tail2
                            Nonterminal("<assn_stmt>", [identNode; assnNode; expNode]), listRest
                        |_ -> failwith ("Expected ASSN_OP got" + sprintf "%A" token2)
            |_ -> failwith ("Expected IDENT got" + sprintf "%A" token)
                
                            
                        
let rec stmt_rest toklexList =
    match toklexList with
    |[] ->
        Nonterminal("<stmt_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |NEWLINE ->
                let newLineNode = Terminal(token, lexeme)
                let stmtNode, listRest1 = stmt tail
                let stmtRestNode, listRest2 = stmt_rest listRest1
                Nonterminal("<stmt_rest>", [newLineNode; stmtNode; stmtRestNode]), listRest2
            |_ -> 
                Nonterminal("<stmt_rest", [Terminal(EMPTY, "empty")]), toklexList

and stmt toklexList =
    match toklexList with
    |[] -> failwith "Empty List"
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |IF ->
                let ifNode, listRest = if_state toklexList
                Nonterminal("<stmt>", [ifNode]), listRest
            |IDENT ->
                let assnNode, listRest = assn_stmt toklexList
                Nonterminal("<stmt>", [assnNode]), listRest
            |_ -> failwith ("Expected IF or IDENT got" + sprintf "%A" token)

and if_state toklexList = 
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |IF ->
                let ifNode = Terminal(token, lexeme)
                match tail with
                |[] -> failwith "If statement not complete"
                |head2::tail2 ->
                    match head2 with
                    |token2,lexeme2 ->
                        match token2 with
                        |OPEN_PAREN ->
                            let openNode = Terminal(token2, lexeme2)
                            let expNode, listRest1 = exp tail2
                            match listRest1 with
                            |[] -> failwith "If statement not complete"
                            |head3::tail3 ->
                                match head3 with
                                |token3,lexeme3 ->
                                    match token3 with
                                    |CLOSED_PAREN ->
                                        let closedNode = Terminal(token3, lexeme3)
                                        let insideNode, listRest2 = inside_if tail3
                                        let ifRestNode, listRest3 = if_rest listRest2
                                        Nonterminal("<if_state>", [ifNode; openNode; expNode; closedNode; insideNode; ifRestNode]), listRest3
                                    |_ -> failwith ("Expected CLOSED_PAREN got" + sprintf "%A" token3)
                        |_ -> failwith ("Expected OPEN_PAREN got" + sprintf "%A" token2)
              |_ -> failwith ("Expected IF got" + sprintf "%A" token)


and inside_if toklexList =
    match toklexList with
    |[] -> failwith "Empty list"
    |head::tail -> 
        match head with
        |token,lexeme ->
            match token with
            |OPEN_BRACKET ->
                let openNode = Terminal(token, lexeme)
                let stmtBlockNode, listRest = stmt_block tail
                match listRest with
                |[] -> failwith "Empty list"
                |head2::tail2 ->
                    match head2 with
                    |token2,lexeme2 ->
                        match token2 with
                        |CLOSED_BRACKET ->
                            let closedNode = Terminal(token2, lexeme2)
                            Nonterminal("<inside_if>", [openNode; stmtBlockNode; closedNode]), tail2
                        |_ -> failwith ("Expected CLOSED_BRACKET got" + sprintf "%A" token2)
            |_ -> failwith ("Expected OPEN_BRACKET got" + sprintf "%A" token)


 and if_rest toklexList =
    match toklexList with
    |[] ->
        Nonterminal("<if_rest", [Terminal(EMPTY, "empty")]), toklexList
    |head::tail ->
        match head with
        |token,lexeme ->
            match token with
            |ELIF ->
                let elifNode = Terminal(token, lexeme)
                match tail with
                |[] -> failwith "Empty list"
                |head2::tail2 ->
                    match head2 with
                    |token2,lexeme2 ->
                        match token2 with
                        |OPEN_PAREN ->
                            let openNode = Terminal(token2, lexeme2)
                            let expNode, listRest1 = exp tail2
                            match listRest1 with
                            |[] -> failwith "Empty list"
                            |head3::tail3 ->
                                match head3 with
                                |token3,lexeme3 ->
                                    match token3 with
                                    |CLOSED_PAREN ->
                                        let closedNode = Terminal(token3, lexeme3)
                                        let insideNode, listRest2 = inside_if tail3
                                        let ifRestNode, listRest3 = if_rest listRest2
                                        Nonterminal("<if_rest>", [elifNode; openNode; expNode; closedNode; insideNode; ifRestNode]), listRest3
                                    |_ -> failwith ("Expected CLOSED_PAREN got" + sprintf "%A" token3)
                        |_ -> failwith ("Expected OPEN_PAREN got" + sprintf "%A" token2)
            |ELSE ->
                let elseNode = Terminal(token, lexeme)
                let insideNode, listRest = inside_if tail
                Nonterminal("<if_rest>", [elseNode; insideNode]), listRest
            |_ ->
                Nonterminal("<if_rest", [Terminal(EMPTY, "empty")]), toklexList
            
            
 and stmt_block toklexList =
    match toklexList with
    |[] -> failwith "List is empty stmt_block"
    |head::tail ->
        let stmtNode, listRest1 = stmt toklexList
        let stmtRestNode, listRest2 = stmt_rest listRest1
        Nonterminal("<stmt_block>", [stmtNode; stmtRestNode]), listRest2
        
            


//Each state from your state machine
type LexState = 
    |START
    //need your own states here
    |ConstINT_LIT
    |ConstIDENT
    |ConstCOMP_OP
    |ConstAO_OP
    |ConstASSN_OP


//takes the current state and the remaining string, and either:
//makes a recursive call (if you stay in the state machine) or
//returns the tuple (token, lexeme, leftOver) where leftOver is the rest of the program still to be parsed
let rec nextLex currState builtString remainingProgStr =  
    match remainingProgStr with 
    |"" -> 
        match currState with
            |ConstINT_LIT -> INT_LIT, builtString, ""
            |ConstIDENT -> IDENT, builtString, ""
            |_ -> ERROR, "", ""
    |_ -> 
        let currChar = remainingProgStr.[0]
        let currString = string currChar
        let leftOver = remainingProgStr.[1..]

        //.... TODO ........ //
        match currState with
        |START ->
            match currChar with
            |currChar when (currChar >= '0' && currChar <= '9') -> nextLex (ConstINT_LIT) currString leftOver
            |'=' -> nextLex (ConstASSN_OP) currString leftOver
            |currChar when (currChar >= 'A' && currChar <= 'Z') || (currChar >= 'a' && currChar <= 'z') -> nextLex (ConstIDENT) currString leftOver
            |'+' | '-' -> AS_OP, currString, leftOver
            |'*' | '/' -> MD_OP, currString, leftOver
            |'&' | '|' -> nextLex (ConstAO_OP) currString leftOver
            |'!' | '<' | '>' -> nextLex (ConstCOMP_OP) currString leftOver
            |'\n' -> NEWLINE, currString, leftOver
            |'{' -> OPEN_BRACKET, currString, leftOver
            |'}' -> CLOSED_BRACKET, currString, leftOver
            |'(' -> OPEN_PAREN, currString, leftOver
            |')' -> CLOSED_PAREN, currString, leftOver
            |' ' -> nextLex (START) "" leftOver
            |_ -> EMPTY, currChar.ToString(), leftOver
        |ConstINT_LIT ->
            match currChar with
            |currChar when (currChar >= '0' && currChar <= '9') -> nextLex (ConstINT_LIT) (builtString + currString) leftOver
            |_ -> INT_LIT, builtString, (currString + leftOver)
        |ConstASSN_OP ->
            match currChar with
            |'=' -> COMP_OP, (builtString + currString), leftOver
            |_ -> ASSN_OP, builtString, (currString + leftOver)
        |ConstIDENT ->
            match currChar with
            |currChar when (currChar >= 'A' && currChar <= 'Z') || (currChar >= 'a' && currChar <= 'z') -> nextLex (ConstIDENT) (builtString + currString) leftOver
            |currChar when (currChar >= '0' && currChar <= '9') -> nextLex (ConstIDENT) (builtString + currString) leftOver
            |_ ->
                match builtString with
                |"if" -> IF, builtString, leftOver
                |"elif" -> ELIF, builtString, leftOver
                |"else" -> ELSE, builtString, leftOver
                |"true" | "false" -> BOOL_LIT, builtString, (currString + leftOver)
                |_ -> IDENT, builtString, (currString + leftOver)
        |ConstAO_OP ->
            match currChar with
            |'&' ->
                match builtString with
                |"&" -> AO_OP, (builtString + currString), leftOver
                |_ -> ERROR, (builtString + currString), leftOver
            |'|' ->
                match builtString with
                |"|" -> AO_OP, (builtString + currString), leftOver
                |_ -> ERROR, (builtString + currString), leftOver
            |_ -> ERROR, builtString, (currString + leftOver)
        |ConstCOMP_OP ->
            match currChar with
            |'=' -> COMP_OP, (builtString + currString), leftOver
            |_ -> 
                match builtString with
                |">"|"<" -> COMP_OP, builtString, (currString + leftOver)
                |"!" -> NOT_OP, builtString, (currString + leftOver)
                |_ -> ERROR, builtString, (currString + leftOver)
           

        




//tests the lexer by calling it repeatedly until entire string has been lexed,
// and returning the list of (token, lexeme) pairs
let testLexer program = 
    //recursive function
    let rec testLexerHelper remainingProgram currLexList = 
        let token, lexeme, rest = nextLex START "" remainingProgram
        match rest with
            |"" ->List.rev ((token, lexeme)::currLexList)
            |_ -> testLexerHelper rest ((token, lexeme)::currLexList)
    //stub function
    testLexerHelper program []

//reads an entire text file into a string (need to use full file path)
let progString = System.IO.File.ReadAllText "C:\Users\DJ\Documents\Visual Studio 2010\Projects\SampleProgram2.txt"
//let progString = "x = 5 \n y = 2"
//calls the tester
let lexList = testLexer progString
let tree, listRemain = stmt_block lexList
let ans = treeToString tree ""
printf "%s" ans
