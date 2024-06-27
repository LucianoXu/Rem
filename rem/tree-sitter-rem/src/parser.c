#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 15
#define LARGE_STATE_COUNT 11
#define SYMBOL_COUNT 65
#define ALIAS_COUNT 0
#define TOKEN_COUNT 56
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 3
#define PRODUCTION_ID_COUNT 1

enum {
  sym_full_stop = 1,
  anon_sym_SLASH_SLASH = 2,
  aux_sym_line_comment_token1 = 3,
  anon_sym_SLASH_STAR = 4,
  aux_sym_block_comment_token1 = 5,
  anon_sym_SLASH = 6,
  anon_sym_abort = 7,
  anon_sym_skip = 8,
  anon_sym_assert = 9,
  anon_sym_if = 10,
  anon_sym_then = 11,
  anon_sym_else = 12,
  anon_sym_end = 13,
  anon_sym_while = 14,
  anon_sym_do = 15,
  anon_sym_Refine = 16,
  anon_sym_End = 17,
  anon_sym_Choose = 18,
  anon_sym_Step = 19,
  anon_sym_Seq = 20,
  anon_sym_If = 21,
  anon_sym_While = 22,
  anon_sym_Inv = 23,
  anon_sym_WeakenPre = 24,
  anon_sym_StrengthenPost = 25,
  anon_sym_Var = 26,
  anon_sym_Def = 27,
  anon_sym_Extract = 28,
  anon_sym_Import = 29,
  anon_sym_Show = 30,
  anon_sym_Eval = 31,
  anon_sym_Test = 32,
  anon_sym_ = 33,
  aux_sym_operator_token1 = 34,
  anon_sym_PLUS = 35,
  anon_sym_DASH = 36,
  anon_sym_STAR = 37,
  anon_sym_2 = 38,
  aux_sym_operator_token2 = 39,
  anon_sym_3 = 40,
  aux_sym_operator_token3 = 41,
  anon_sym_4 = 42,
  aux_sym_operator_token4 = 43,
  anon_sym_5 = 44,
  aux_sym_operator_token5 = 45,
  anon_sym_CARET = 46,
  aux_sym_operator_token6 = 47,
  anon_sym_6 = 48,
  aux_sym_operator_token7 = 49,
  anon_sym_7 = 50,
  aux_sym_operator_token8 = 51,
  sym_identifier = 52,
  anon_sym_IQOpt = 53,
  anon_sym_QOpt = 54,
  anon_sym_QProg = 55,
  sym_document = 56,
  sym_cmd = 57,
  sym_line_comment = 58,
  sym_block_comment = 59,
  sym_prog_keyword = 60,
  sym_keyword = 61,
  sym_operator = 62,
  sym_types = 63,
  aux_sym_document_repeat1 = 64,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_full_stop] = "full_stop",
  [anon_sym_SLASH_SLASH] = "//",
  [aux_sym_line_comment_token1] = "line_comment_token1",
  [anon_sym_SLASH_STAR] = "/*",
  [aux_sym_block_comment_token1] = "block_comment_token1",
  [anon_sym_SLASH] = "/",
  [anon_sym_abort] = "abort",
  [anon_sym_skip] = "skip",
  [anon_sym_assert] = "assert",
  [anon_sym_if] = "if",
  [anon_sym_then] = "then",
  [anon_sym_else] = "else",
  [anon_sym_end] = "end",
  [anon_sym_while] = "while",
  [anon_sym_do] = "do",
  [anon_sym_Refine] = "Refine",
  [anon_sym_End] = "End",
  [anon_sym_Choose] = "Choose",
  [anon_sym_Step] = "Step",
  [anon_sym_Seq] = "Seq",
  [anon_sym_If] = "If",
  [anon_sym_While] = "While",
  [anon_sym_Inv] = "Inv",
  [anon_sym_WeakenPre] = "WeakenPre",
  [anon_sym_StrengthenPost] = "StrengthenPost",
  [anon_sym_Var] = "Var",
  [anon_sym_Def] = "Def",
  [anon_sym_Extract] = "Extract",
  [anon_sym_Import] = "Import",
  [anon_sym_Show] = "Show",
  [anon_sym_Eval] = "Eval",
  [anon_sym_Test] = "Test",
  [anon_sym_] = "⊕",
  [aux_sym_operator_token1] = "operator_token1",
  [anon_sym_PLUS] = "+",
  [anon_sym_DASH] = "-",
  [anon_sym_STAR] = "*",
  [anon_sym_2] = "⊗",
  [aux_sym_operator_token2] = "operator_token2",
  [anon_sym_3] = "†",
  [aux_sym_operator_token3] = "operator_token3",
  [anon_sym_4] = "∨",
  [aux_sym_operator_token4] = "operator_token4",
  [anon_sym_5] = "∧",
  [aux_sym_operator_token5] = "operator_token5",
  [anon_sym_CARET] = "^⊥",
  [aux_sym_operator_token6] = "operator_token6",
  [anon_sym_6] = "⇝",
  [aux_sym_operator_token7] = "operator_token7",
  [anon_sym_7] = "⋒",
  [aux_sym_operator_token8] = "operator_token8",
  [sym_identifier] = "identifier",
  [anon_sym_IQOpt] = "IQOpt",
  [anon_sym_QOpt] = "QOpt",
  [anon_sym_QProg] = "QProg",
  [sym_document] = "document",
  [sym_cmd] = "cmd",
  [sym_line_comment] = "line_comment",
  [sym_block_comment] = "block_comment",
  [sym_prog_keyword] = "prog_keyword",
  [sym_keyword] = "keyword",
  [sym_operator] = "operator",
  [sym_types] = "types",
  [aux_sym_document_repeat1] = "document_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_full_stop] = sym_full_stop,
  [anon_sym_SLASH_SLASH] = anon_sym_SLASH_SLASH,
  [aux_sym_line_comment_token1] = aux_sym_line_comment_token1,
  [anon_sym_SLASH_STAR] = anon_sym_SLASH_STAR,
  [aux_sym_block_comment_token1] = aux_sym_block_comment_token1,
  [anon_sym_SLASH] = anon_sym_SLASH,
  [anon_sym_abort] = anon_sym_abort,
  [anon_sym_skip] = anon_sym_skip,
  [anon_sym_assert] = anon_sym_assert,
  [anon_sym_if] = anon_sym_if,
  [anon_sym_then] = anon_sym_then,
  [anon_sym_else] = anon_sym_else,
  [anon_sym_end] = anon_sym_end,
  [anon_sym_while] = anon_sym_while,
  [anon_sym_do] = anon_sym_do,
  [anon_sym_Refine] = anon_sym_Refine,
  [anon_sym_End] = anon_sym_End,
  [anon_sym_Choose] = anon_sym_Choose,
  [anon_sym_Step] = anon_sym_Step,
  [anon_sym_Seq] = anon_sym_Seq,
  [anon_sym_If] = anon_sym_If,
  [anon_sym_While] = anon_sym_While,
  [anon_sym_Inv] = anon_sym_Inv,
  [anon_sym_WeakenPre] = anon_sym_WeakenPre,
  [anon_sym_StrengthenPost] = anon_sym_StrengthenPost,
  [anon_sym_Var] = anon_sym_Var,
  [anon_sym_Def] = anon_sym_Def,
  [anon_sym_Extract] = anon_sym_Extract,
  [anon_sym_Import] = anon_sym_Import,
  [anon_sym_Show] = anon_sym_Show,
  [anon_sym_Eval] = anon_sym_Eval,
  [anon_sym_Test] = anon_sym_Test,
  [anon_sym_] = anon_sym_,
  [aux_sym_operator_token1] = aux_sym_operator_token1,
  [anon_sym_PLUS] = anon_sym_PLUS,
  [anon_sym_DASH] = anon_sym_DASH,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_2] = anon_sym_2,
  [aux_sym_operator_token2] = aux_sym_operator_token2,
  [anon_sym_3] = anon_sym_3,
  [aux_sym_operator_token3] = aux_sym_operator_token3,
  [anon_sym_4] = anon_sym_4,
  [aux_sym_operator_token4] = aux_sym_operator_token4,
  [anon_sym_5] = anon_sym_5,
  [aux_sym_operator_token5] = aux_sym_operator_token5,
  [anon_sym_CARET] = anon_sym_CARET,
  [aux_sym_operator_token6] = aux_sym_operator_token6,
  [anon_sym_6] = anon_sym_6,
  [aux_sym_operator_token7] = aux_sym_operator_token7,
  [anon_sym_7] = anon_sym_7,
  [aux_sym_operator_token8] = aux_sym_operator_token8,
  [sym_identifier] = sym_identifier,
  [anon_sym_IQOpt] = anon_sym_IQOpt,
  [anon_sym_QOpt] = anon_sym_QOpt,
  [anon_sym_QProg] = anon_sym_QProg,
  [sym_document] = sym_document,
  [sym_cmd] = sym_cmd,
  [sym_line_comment] = sym_line_comment,
  [sym_block_comment] = sym_block_comment,
  [sym_prog_keyword] = sym_prog_keyword,
  [sym_keyword] = sym_keyword,
  [sym_operator] = sym_operator,
  [sym_types] = sym_types,
  [aux_sym_document_repeat1] = aux_sym_document_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_full_stop] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_SLASH_SLASH] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_line_comment_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_SLASH_STAR] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_block_comment_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_SLASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_abort] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_skip] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_assert] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_if] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_then] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_else] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_end] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_while] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_do] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Refine] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_End] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Choose] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Step] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Seq] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_If] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_While] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Inv] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WeakenPre] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_StrengthenPost] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Var] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Def] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Extract] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Import] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Show] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Eval] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_Test] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_PLUS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_2] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token2] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_3] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token3] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_4] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token4] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_5] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token5] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_CARET] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token6] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_6] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token7] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_7] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_operator_token8] = {
    .visible = false,
    .named = false,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_IQOpt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_QOpt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_QProg] = {
    .visible = true,
    .named = false,
  },
  [sym_document] = {
    .visible = true,
    .named = true,
  },
  [sym_cmd] = {
    .visible = true,
    .named = true,
  },
  [sym_line_comment] = {
    .visible = true,
    .named = true,
  },
  [sym_block_comment] = {
    .visible = true,
    .named = true,
  },
  [sym_prog_keyword] = {
    .visible = true,
    .named = true,
  },
  [sym_keyword] = {
    .visible = true,
    .named = true,
  },
  [sym_operator] = {
    .visible = true,
    .named = true,
  },
  [sym_types] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_document_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(47);
      if (lookahead == '*') ADVANCE(85);
      if (lookahead == '+') ADVANCE(83);
      if (lookahead == '-') ADVANCE(84);
      if (lookahead == '.') ADVANCE(48);
      if (lookahead == '/') ADVANCE(54);
      if (lookahead == 'C') ADVANCE(135);
      if (lookahead == 'D') ADVANCE(122);
      if (lookahead == 'E') ADVANCE(149);
      if (lookahead == 'I') ADVANCE(104);
      if (lookahead == 'Q') ADVANCE(100);
      if (lookahead == 'R') ADVANCE(124);
      if (lookahead == 'S') ADVANCE(113);
      if (lookahead == 'T') ADVANCE(114);
      if (lookahead == 'V') ADVANCE(108);
      if (lookahead == 'W') ADVANCE(123);
      if (lookahead == '\\') ADVANCE(5);
      if (lookahead == '^') ADVANCE(6);
      if (lookahead == 'a') ADVANCE(109);
      if (lookahead == 'd') ADVANCE(155);
      if (lookahead == 'e') ADVANCE(148);
      if (lookahead == 'i') ADVANCE(130);
      if (lookahead == 's') ADVANCE(143);
      if (lookahead == 't') ADVANCE(136);
      if (lookahead == 'w') ADVANCE(138);
      if (lookahead == 8224) ADVANCE(88);
      if (lookahead == 8669) ADVANCE(96);
      if (lookahead == 8743) ADVANCE(92);
      if (lookahead == 8744) ADVANCE(90);
      if (lookahead == 8853) ADVANCE(81);
      if (lookahead == 8855) ADVANCE(86);
      if (lookahead == 8914) ADVANCE(98);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (lookahead == '\'' ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 1:
      if (lookahead == '*') ADVANCE(52);
      if (lookahead == '/') ADVANCE(49);
      END_STATE();
    case 2:
      if (lookahead == '*') ADVANCE(53);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(2);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 3:
      if (lookahead == '*') ADVANCE(53);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 4:
      if (lookahead == 'C') ADVANCE(33);
      if (lookahead == 'I') ADVANCE(29);
      END_STATE();
    case 5:
      if (lookahead == 'S') ADVANCE(7);
      if (lookahead == 'o') ADVANCE(34);
      if (lookahead == 'v') ADVANCE(18);
      if (lookahead == 'w') ADVANCE(13);
      END_STATE();
    case 6:
      if (lookahead == '\\') ADVANCE(12);
      if (lookahead == 8869) ADVANCE(94);
      END_STATE();
    case 7:
      if (lookahead == 'a') ADVANCE(41);
      END_STATE();
    case 8:
      if (lookahead == 'a') ADVANCE(26);
      END_STATE();
    case 9:
      if (lookahead == 'a') ADVANCE(22);
      END_STATE();
    case 10:
      if (lookahead == 'c') ADVANCE(42);
      END_STATE();
    case 11:
      if (lookahead == 'd') ADVANCE(20);
      END_STATE();
    case 12:
      if (lookahead == 'd') ADVANCE(9);
      if (lookahead == 'p') ADVANCE(15);
      END_STATE();
    case 13:
      if (lookahead == 'e') ADVANCE(11);
      END_STATE();
    case 14:
      if (lookahead == 'e') ADVANCE(91);
      END_STATE();
    case 15:
      if (lookahead == 'e') ADVANCE(37);
      END_STATE();
    case 16:
      if (lookahead == 'e') ADVANCE(93);
      END_STATE();
    case 17:
      if (lookahead == 'e') ADVANCE(38);
      END_STATE();
    case 18:
      if (lookahead == 'e') ADVANCE(14);
      END_STATE();
    case 19:
      if (lookahead == 'e') ADVANCE(40);
      END_STATE();
    case 20:
      if (lookahead == 'g') ADVANCE(16);
      END_STATE();
    case 21:
      if (lookahead == 'g') ADVANCE(17);
      END_STATE();
    case 22:
      if (lookahead == 'g') ADVANCE(21);
      END_STATE();
    case 23:
      if (lookahead == 'i') ADVANCE(30);
      END_STATE();
    case 24:
      if (lookahead == 'i') ADVANCE(4);
      END_STATE();
    case 25:
      if (lookahead == 'j') ADVANCE(44);
      END_STATE();
    case 26:
      if (lookahead == 'k') ADVANCE(24);
      END_STATE();
    case 27:
      if (lookahead == 'l') ADVANCE(43);
      END_STATE();
    case 28:
      if (lookahead == 'l') ADVANCE(45);
      END_STATE();
    case 29:
      if (lookahead == 'm') ADVANCE(36);
      END_STATE();
    case 30:
      if (lookahead == 'm') ADVANCE(19);
      END_STATE();
    case 31:
      if (lookahead == 'n') ADVANCE(25);
      END_STATE();
    case 32:
      if (lookahead == 'n') ADVANCE(10);
      END_STATE();
    case 33:
      if (lookahead == 'o') ADVANCE(31);
      END_STATE();
    case 34:
      if (lookahead == 'p') ADVANCE(27);
      if (lookahead == 't') ADVANCE(23);
      END_STATE();
    case 35:
      if (lookahead == 'p') ADVANCE(95);
      END_STATE();
    case 36:
      if (lookahead == 'p') ADVANCE(28);
      END_STATE();
    case 37:
      if (lookahead == 'r') ADVANCE(35);
      END_STATE();
    case 38:
      if (lookahead == 'r') ADVANCE(89);
      END_STATE();
    case 39:
      if (lookahead == 's') ADVANCE(82);
      END_STATE();
    case 40:
      if (lookahead == 's') ADVANCE(87);
      END_STATE();
    case 41:
      if (lookahead == 's') ADVANCE(8);
      END_STATE();
    case 42:
      if (lookahead == 't') ADVANCE(99);
      END_STATE();
    case 43:
      if (lookahead == 'u') ADVANCE(39);
      END_STATE();
    case 44:
      if (lookahead == 'u') ADVANCE(32);
      END_STATE();
    case 45:
      if (lookahead == 'y') ADVANCE(97);
      END_STATE();
    case 46:
      if (eof) ADVANCE(47);
      if (lookahead == '*') ADVANCE(85);
      if (lookahead == '+') ADVANCE(83);
      if (lookahead == '-') ADVANCE(84);
      if (lookahead == '.') ADVANCE(48);
      if (lookahead == '/') ADVANCE(1);
      if (lookahead == 'C') ADVANCE(135);
      if (lookahead == 'D') ADVANCE(122);
      if (lookahead == 'E') ADVANCE(149);
      if (lookahead == 'I') ADVANCE(104);
      if (lookahead == 'Q') ADVANCE(100);
      if (lookahead == 'R') ADVANCE(124);
      if (lookahead == 'S') ADVANCE(113);
      if (lookahead == 'T') ADVANCE(114);
      if (lookahead == 'V') ADVANCE(108);
      if (lookahead == 'W') ADVANCE(123);
      if (lookahead == '\\') ADVANCE(5);
      if (lookahead == '^') ADVANCE(6);
      if (lookahead == 'a') ADVANCE(109);
      if (lookahead == 'd') ADVANCE(155);
      if (lookahead == 'e') ADVANCE(148);
      if (lookahead == 'i') ADVANCE(130);
      if (lookahead == 's') ADVANCE(143);
      if (lookahead == 't') ADVANCE(136);
      if (lookahead == 'w') ADVANCE(138);
      if (lookahead == 8224) ADVANCE(88);
      if (lookahead == 8669) ADVANCE(96);
      if (lookahead == 8743) ADVANCE(92);
      if (lookahead == 8744) ADVANCE(90);
      if (lookahead == 8853) ADVANCE(81);
      if (lookahead == 8855) ADVANCE(86);
      if (lookahead == 8914) ADVANCE(98);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(46)
      if (lookahead == '\'' ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_full_stop);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(anon_sym_SLASH_SLASH);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(aux_sym_line_comment_token1);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(50);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(51);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(aux_sym_line_comment_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(51);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(anon_sym_SLASH_STAR);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(aux_sym_block_comment_token1);
      if (lookahead == '*') ADVANCE(53);
      if (lookahead != 0 &&
          lookahead != '/') ADVANCE(3);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(anon_sym_abort);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(anon_sym_skip);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(anon_sym_assert);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(anon_sym_if);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(anon_sym_then);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(anon_sym_else);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(anon_sym_end);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(anon_sym_while);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(anon_sym_do);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(anon_sym_Refine);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(anon_sym_End);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(anon_sym_Choose);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(anon_sym_Step);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(anon_sym_Seq);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(anon_sym_If);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(anon_sym_While);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(anon_sym_Inv);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(anon_sym_WeakenPre);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(anon_sym_StrengthenPost);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(anon_sym_Var);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(anon_sym_Def);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(anon_sym_Extract);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(anon_sym_Import);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(anon_sym_Show);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(anon_sym_Eval);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(anon_sym_Test);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(anon_sym_);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(aux_sym_operator_token1);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(anon_sym_PLUS);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(anon_sym_2);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(aux_sym_operator_token2);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(anon_sym_3);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(aux_sym_operator_token3);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(anon_sym_4);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(aux_sym_operator_token4);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(anon_sym_5);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(aux_sym_operator_token5);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(anon_sym_CARET);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(aux_sym_operator_token6);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(anon_sym_6);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(aux_sym_operator_token7);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(anon_sym_7);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(aux_sym_operator_token8);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(165);
      if (lookahead == 'P') ADVANCE(172);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(166);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'P') ADVANCE(175);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'P') ADVANCE(160);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'Q') ADVANCE(101);
      if (lookahead == 'f') ADVANCE(69);
      if (lookahead == 'm') ADVANCE(167);
      if (lookahead == 'n') ADVANCE(191);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(145);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(110);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(144);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(169);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'b') ADVANCE(158);
      if (lookahead == 's') ADVANCE(177);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'c') ADVANCE(187);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 111:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'd') ADVANCE(65);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 112:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'd') ADVANCE(61);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 113:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(168);
      if (lookahead == 'h') ADVANCE(156);
      if (lookahead == 't') ADVANCE(126);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 114:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(176);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 115:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(150);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 116:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(60);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 117:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(70);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 118:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(62);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 119:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(66);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 120:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(64);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 121:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(72);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 122:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(131);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 123:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(107);
      if (lookahead == 'h') ADVANCE(139);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 124:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(132);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 125:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(152);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 126:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(163);
      if (lookahead == 'r') ADVANCE(125);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 127:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(151);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 128:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(153);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 129:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(174);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 130:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'f') ADVANCE(58);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 131:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'f') ADVANCE(75);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 132:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'f') ADVANCE(140);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 133:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'g') ADVANCE(196);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 134:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'g') ADVANCE(190);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 135:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'h') ADVANCE(159);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 136:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'h') ADVANCE(115);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 137:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'h') ADVANCE(128);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 138:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'h') ADVANCE(142);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 139:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(146);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 140:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(154);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 141:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(164);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 142:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(147);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 143:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'k') ADVANCE(141);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 144:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'k') ADVANCE(127);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 145:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(79);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 146:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(117);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 147:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(118);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 148:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(178);
      if (lookahead == 'n') ADVANCE(112);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 149:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(111);
      if (lookahead == 'v') ADVANCE(105);
      if (lookahead == 'x') ADVANCE(189);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 150:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(59);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 151:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(102);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 152:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(134);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 153:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(103);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 154:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(120);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 155:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(63);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 156:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(192);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 157:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(133);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 158:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(171);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 159:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(162);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 160:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(180);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 161:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(173);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 162:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(179);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 163:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'p') ADVANCE(67);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 164:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'p') ADVANCE(56);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 165:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'p') ADVANCE(181);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 166:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'p') ADVANCE(183);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 167:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'p') ADVANCE(161);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 168:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'q') ADVANCE(68);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 169:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(74);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 170:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(106);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 171:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(184);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 172:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(157);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 173:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(185);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 174:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(186);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 175:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'r') ADVANCE(121);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 176:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(182);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 177:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(129);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 178:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(116);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 179:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(119);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 180:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(188);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 181:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(195);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 182:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(80);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 183:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(194);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 184:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(55);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 185:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(77);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 186:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(57);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 187:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(76);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 188:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(73);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 189:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(170);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 190:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(137);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 191:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'v') ADVANCE(71);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 192:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'w') ADVANCE(78);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 193:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 194:
      ACCEPT_TOKEN(anon_sym_IQOpt);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 195:
      ACCEPT_TOKEN(anon_sym_QOpt);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    case 196:
      ACCEPT_TOKEN(anon_sym_QProg);
      if (lookahead == '\'' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(193);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 46},
  [2] = {.lex_state = 46},
  [3] = {.lex_state = 46},
  [4] = {.lex_state = 46},
  [5] = {.lex_state = 46},
  [6] = {.lex_state = 46},
  [7] = {.lex_state = 46},
  [8] = {.lex_state = 46},
  [9] = {.lex_state = 46},
  [10] = {.lex_state = 46},
  [11] = {.lex_state = 50},
  [12] = {.lex_state = 2},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_full_stop] = ACTIONS(1),
    [anon_sym_SLASH] = ACTIONS(1),
    [anon_sym_abort] = ACTIONS(1),
    [anon_sym_skip] = ACTIONS(1),
    [anon_sym_assert] = ACTIONS(1),
    [anon_sym_if] = ACTIONS(1),
    [anon_sym_then] = ACTIONS(1),
    [anon_sym_else] = ACTIONS(1),
    [anon_sym_end] = ACTIONS(1),
    [anon_sym_while] = ACTIONS(1),
    [anon_sym_do] = ACTIONS(1),
    [anon_sym_Refine] = ACTIONS(1),
    [anon_sym_End] = ACTIONS(1),
    [anon_sym_Choose] = ACTIONS(1),
    [anon_sym_Step] = ACTIONS(1),
    [anon_sym_Seq] = ACTIONS(1),
    [anon_sym_If] = ACTIONS(1),
    [anon_sym_While] = ACTIONS(1),
    [anon_sym_Inv] = ACTIONS(1),
    [anon_sym_WeakenPre] = ACTIONS(1),
    [anon_sym_StrengthenPost] = ACTIONS(1),
    [anon_sym_Var] = ACTIONS(1),
    [anon_sym_Def] = ACTIONS(1),
    [anon_sym_Extract] = ACTIONS(1),
    [anon_sym_Import] = ACTIONS(1),
    [anon_sym_Show] = ACTIONS(1),
    [anon_sym_Eval] = ACTIONS(1),
    [anon_sym_Test] = ACTIONS(1),
    [anon_sym_] = ACTIONS(1),
    [aux_sym_operator_token1] = ACTIONS(1),
    [anon_sym_PLUS] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_2] = ACTIONS(1),
    [aux_sym_operator_token2] = ACTIONS(1),
    [anon_sym_3] = ACTIONS(1),
    [aux_sym_operator_token3] = ACTIONS(1),
    [anon_sym_4] = ACTIONS(1),
    [aux_sym_operator_token4] = ACTIONS(1),
    [anon_sym_5] = ACTIONS(1),
    [aux_sym_operator_token5] = ACTIONS(1),
    [anon_sym_CARET] = ACTIONS(1),
    [aux_sym_operator_token6] = ACTIONS(1),
    [anon_sym_6] = ACTIONS(1),
    [aux_sym_operator_token7] = ACTIONS(1),
    [anon_sym_7] = ACTIONS(1),
    [aux_sym_operator_token8] = ACTIONS(1),
    [sym_identifier] = ACTIONS(1),
    [anon_sym_IQOpt] = ACTIONS(1),
    [anon_sym_QOpt] = ACTIONS(1),
    [anon_sym_QProg] = ACTIONS(1),
  },
  [1] = {
    [sym_document] = STATE(13),
    [sym_cmd] = STATE(2),
    [sym_line_comment] = STATE(4),
    [sym_block_comment] = STATE(4),
    [sym_prog_keyword] = STATE(4),
    [sym_keyword] = STATE(4),
    [sym_operator] = STATE(4),
    [sym_types] = STATE(4),
    [aux_sym_document_repeat1] = STATE(2),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_full_stop] = ACTIONS(5),
    [anon_sym_SLASH_SLASH] = ACTIONS(7),
    [anon_sym_SLASH_STAR] = ACTIONS(9),
    [anon_sym_abort] = ACTIONS(11),
    [anon_sym_skip] = ACTIONS(11),
    [anon_sym_assert] = ACTIONS(11),
    [anon_sym_if] = ACTIONS(11),
    [anon_sym_then] = ACTIONS(11),
    [anon_sym_else] = ACTIONS(11),
    [anon_sym_end] = ACTIONS(11),
    [anon_sym_while] = ACTIONS(11),
    [anon_sym_do] = ACTIONS(11),
    [anon_sym_Refine] = ACTIONS(13),
    [anon_sym_End] = ACTIONS(13),
    [anon_sym_Choose] = ACTIONS(13),
    [anon_sym_Step] = ACTIONS(13),
    [anon_sym_Seq] = ACTIONS(13),
    [anon_sym_If] = ACTIONS(13),
    [anon_sym_While] = ACTIONS(13),
    [anon_sym_Inv] = ACTIONS(13),
    [anon_sym_WeakenPre] = ACTIONS(13),
    [anon_sym_StrengthenPost] = ACTIONS(13),
    [anon_sym_Var] = ACTIONS(13),
    [anon_sym_Def] = ACTIONS(13),
    [anon_sym_Extract] = ACTIONS(13),
    [anon_sym_Import] = ACTIONS(13),
    [anon_sym_Show] = ACTIONS(13),
    [anon_sym_Eval] = ACTIONS(13),
    [anon_sym_Test] = ACTIONS(13),
    [anon_sym_] = ACTIONS(15),
    [aux_sym_operator_token1] = ACTIONS(15),
    [anon_sym_PLUS] = ACTIONS(15),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(15),
    [anon_sym_2] = ACTIONS(15),
    [aux_sym_operator_token2] = ACTIONS(15),
    [anon_sym_3] = ACTIONS(15),
    [aux_sym_operator_token3] = ACTIONS(15),
    [anon_sym_4] = ACTIONS(15),
    [aux_sym_operator_token4] = ACTIONS(15),
    [anon_sym_5] = ACTIONS(15),
    [aux_sym_operator_token5] = ACTIONS(15),
    [anon_sym_CARET] = ACTIONS(15),
    [aux_sym_operator_token6] = ACTIONS(15),
    [anon_sym_6] = ACTIONS(15),
    [aux_sym_operator_token7] = ACTIONS(15),
    [anon_sym_7] = ACTIONS(15),
    [aux_sym_operator_token8] = ACTIONS(15),
    [sym_identifier] = ACTIONS(17),
    [anon_sym_IQOpt] = ACTIONS(19),
    [anon_sym_QOpt] = ACTIONS(19),
    [anon_sym_QProg] = ACTIONS(19),
  },
  [2] = {
    [sym_cmd] = STATE(3),
    [sym_line_comment] = STATE(4),
    [sym_block_comment] = STATE(4),
    [sym_prog_keyword] = STATE(4),
    [sym_keyword] = STATE(4),
    [sym_operator] = STATE(4),
    [sym_types] = STATE(4),
    [aux_sym_document_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(21),
    [sym_full_stop] = ACTIONS(5),
    [anon_sym_SLASH_SLASH] = ACTIONS(7),
    [anon_sym_SLASH_STAR] = ACTIONS(9),
    [anon_sym_abort] = ACTIONS(11),
    [anon_sym_skip] = ACTIONS(11),
    [anon_sym_assert] = ACTIONS(11),
    [anon_sym_if] = ACTIONS(11),
    [anon_sym_then] = ACTIONS(11),
    [anon_sym_else] = ACTIONS(11),
    [anon_sym_end] = ACTIONS(11),
    [anon_sym_while] = ACTIONS(11),
    [anon_sym_do] = ACTIONS(11),
    [anon_sym_Refine] = ACTIONS(13),
    [anon_sym_End] = ACTIONS(13),
    [anon_sym_Choose] = ACTIONS(13),
    [anon_sym_Step] = ACTIONS(13),
    [anon_sym_Seq] = ACTIONS(13),
    [anon_sym_If] = ACTIONS(13),
    [anon_sym_While] = ACTIONS(13),
    [anon_sym_Inv] = ACTIONS(13),
    [anon_sym_WeakenPre] = ACTIONS(13),
    [anon_sym_StrengthenPost] = ACTIONS(13),
    [anon_sym_Var] = ACTIONS(13),
    [anon_sym_Def] = ACTIONS(13),
    [anon_sym_Extract] = ACTIONS(13),
    [anon_sym_Import] = ACTIONS(13),
    [anon_sym_Show] = ACTIONS(13),
    [anon_sym_Eval] = ACTIONS(13),
    [anon_sym_Test] = ACTIONS(13),
    [anon_sym_] = ACTIONS(15),
    [aux_sym_operator_token1] = ACTIONS(15),
    [anon_sym_PLUS] = ACTIONS(15),
    [anon_sym_DASH] = ACTIONS(15),
    [anon_sym_STAR] = ACTIONS(15),
    [anon_sym_2] = ACTIONS(15),
    [aux_sym_operator_token2] = ACTIONS(15),
    [anon_sym_3] = ACTIONS(15),
    [aux_sym_operator_token3] = ACTIONS(15),
    [anon_sym_4] = ACTIONS(15),
    [aux_sym_operator_token4] = ACTIONS(15),
    [anon_sym_5] = ACTIONS(15),
    [aux_sym_operator_token5] = ACTIONS(15),
    [anon_sym_CARET] = ACTIONS(15),
    [aux_sym_operator_token6] = ACTIONS(15),
    [anon_sym_6] = ACTIONS(15),
    [aux_sym_operator_token7] = ACTIONS(15),
    [anon_sym_7] = ACTIONS(15),
    [aux_sym_operator_token8] = ACTIONS(15),
    [sym_identifier] = ACTIONS(17),
    [anon_sym_IQOpt] = ACTIONS(19),
    [anon_sym_QOpt] = ACTIONS(19),
    [anon_sym_QProg] = ACTIONS(19),
  },
  [3] = {
    [sym_cmd] = STATE(3),
    [sym_line_comment] = STATE(4),
    [sym_block_comment] = STATE(4),
    [sym_prog_keyword] = STATE(4),
    [sym_keyword] = STATE(4),
    [sym_operator] = STATE(4),
    [sym_types] = STATE(4),
    [aux_sym_document_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(23),
    [sym_full_stop] = ACTIONS(25),
    [anon_sym_SLASH_SLASH] = ACTIONS(28),
    [anon_sym_SLASH_STAR] = ACTIONS(31),
    [anon_sym_abort] = ACTIONS(34),
    [anon_sym_skip] = ACTIONS(34),
    [anon_sym_assert] = ACTIONS(34),
    [anon_sym_if] = ACTIONS(34),
    [anon_sym_then] = ACTIONS(34),
    [anon_sym_else] = ACTIONS(34),
    [anon_sym_end] = ACTIONS(34),
    [anon_sym_while] = ACTIONS(34),
    [anon_sym_do] = ACTIONS(34),
    [anon_sym_Refine] = ACTIONS(37),
    [anon_sym_End] = ACTIONS(37),
    [anon_sym_Choose] = ACTIONS(37),
    [anon_sym_Step] = ACTIONS(37),
    [anon_sym_Seq] = ACTIONS(37),
    [anon_sym_If] = ACTIONS(37),
    [anon_sym_While] = ACTIONS(37),
    [anon_sym_Inv] = ACTIONS(37),
    [anon_sym_WeakenPre] = ACTIONS(37),
    [anon_sym_StrengthenPost] = ACTIONS(37),
    [anon_sym_Var] = ACTIONS(37),
    [anon_sym_Def] = ACTIONS(37),
    [anon_sym_Extract] = ACTIONS(37),
    [anon_sym_Import] = ACTIONS(37),
    [anon_sym_Show] = ACTIONS(37),
    [anon_sym_Eval] = ACTIONS(37),
    [anon_sym_Test] = ACTIONS(37),
    [anon_sym_] = ACTIONS(40),
    [aux_sym_operator_token1] = ACTIONS(40),
    [anon_sym_PLUS] = ACTIONS(40),
    [anon_sym_DASH] = ACTIONS(40),
    [anon_sym_STAR] = ACTIONS(40),
    [anon_sym_2] = ACTIONS(40),
    [aux_sym_operator_token2] = ACTIONS(40),
    [anon_sym_3] = ACTIONS(40),
    [aux_sym_operator_token3] = ACTIONS(40),
    [anon_sym_4] = ACTIONS(40),
    [aux_sym_operator_token4] = ACTIONS(40),
    [anon_sym_5] = ACTIONS(40),
    [aux_sym_operator_token5] = ACTIONS(40),
    [anon_sym_CARET] = ACTIONS(40),
    [aux_sym_operator_token6] = ACTIONS(40),
    [anon_sym_6] = ACTIONS(40),
    [aux_sym_operator_token7] = ACTIONS(40),
    [anon_sym_7] = ACTIONS(40),
    [aux_sym_operator_token8] = ACTIONS(40),
    [sym_identifier] = ACTIONS(43),
    [anon_sym_IQOpt] = ACTIONS(46),
    [anon_sym_QOpt] = ACTIONS(46),
    [anon_sym_QProg] = ACTIONS(46),
  },
  [4] = {
    [ts_builtin_sym_end] = ACTIONS(49),
    [sym_full_stop] = ACTIONS(49),
    [anon_sym_SLASH_SLASH] = ACTIONS(49),
    [anon_sym_SLASH_STAR] = ACTIONS(49),
    [anon_sym_abort] = ACTIONS(51),
    [anon_sym_skip] = ACTIONS(51),
    [anon_sym_assert] = ACTIONS(51),
    [anon_sym_if] = ACTIONS(51),
    [anon_sym_then] = ACTIONS(51),
    [anon_sym_else] = ACTIONS(51),
    [anon_sym_end] = ACTIONS(51),
    [anon_sym_while] = ACTIONS(51),
    [anon_sym_do] = ACTIONS(51),
    [anon_sym_Refine] = ACTIONS(51),
    [anon_sym_End] = ACTIONS(51),
    [anon_sym_Choose] = ACTIONS(51),
    [anon_sym_Step] = ACTIONS(51),
    [anon_sym_Seq] = ACTIONS(51),
    [anon_sym_If] = ACTIONS(51),
    [anon_sym_While] = ACTIONS(51),
    [anon_sym_Inv] = ACTIONS(51),
    [anon_sym_WeakenPre] = ACTIONS(51),
    [anon_sym_StrengthenPost] = ACTIONS(51),
    [anon_sym_Var] = ACTIONS(51),
    [anon_sym_Def] = ACTIONS(51),
    [anon_sym_Extract] = ACTIONS(51),
    [anon_sym_Import] = ACTIONS(51),
    [anon_sym_Show] = ACTIONS(51),
    [anon_sym_Eval] = ACTIONS(51),
    [anon_sym_Test] = ACTIONS(51),
    [anon_sym_] = ACTIONS(49),
    [aux_sym_operator_token1] = ACTIONS(49),
    [anon_sym_PLUS] = ACTIONS(49),
    [anon_sym_DASH] = ACTIONS(49),
    [anon_sym_STAR] = ACTIONS(49),
    [anon_sym_2] = ACTIONS(49),
    [aux_sym_operator_token2] = ACTIONS(49),
    [anon_sym_3] = ACTIONS(49),
    [aux_sym_operator_token3] = ACTIONS(49),
    [anon_sym_4] = ACTIONS(49),
    [aux_sym_operator_token4] = ACTIONS(49),
    [anon_sym_5] = ACTIONS(49),
    [aux_sym_operator_token5] = ACTIONS(49),
    [anon_sym_CARET] = ACTIONS(49),
    [aux_sym_operator_token6] = ACTIONS(49),
    [anon_sym_6] = ACTIONS(49),
    [aux_sym_operator_token7] = ACTIONS(49),
    [anon_sym_7] = ACTIONS(49),
    [aux_sym_operator_token8] = ACTIONS(49),
    [sym_identifier] = ACTIONS(51),
    [anon_sym_IQOpt] = ACTIONS(51),
    [anon_sym_QOpt] = ACTIONS(51),
    [anon_sym_QProg] = ACTIONS(51),
  },
  [5] = {
    [ts_builtin_sym_end] = ACTIONS(53),
    [sym_full_stop] = ACTIONS(53),
    [anon_sym_SLASH_SLASH] = ACTIONS(53),
    [anon_sym_SLASH_STAR] = ACTIONS(53),
    [anon_sym_abort] = ACTIONS(55),
    [anon_sym_skip] = ACTIONS(55),
    [anon_sym_assert] = ACTIONS(55),
    [anon_sym_if] = ACTIONS(55),
    [anon_sym_then] = ACTIONS(55),
    [anon_sym_else] = ACTIONS(55),
    [anon_sym_end] = ACTIONS(55),
    [anon_sym_while] = ACTIONS(55),
    [anon_sym_do] = ACTIONS(55),
    [anon_sym_Refine] = ACTIONS(55),
    [anon_sym_End] = ACTIONS(55),
    [anon_sym_Choose] = ACTIONS(55),
    [anon_sym_Step] = ACTIONS(55),
    [anon_sym_Seq] = ACTIONS(55),
    [anon_sym_If] = ACTIONS(55),
    [anon_sym_While] = ACTIONS(55),
    [anon_sym_Inv] = ACTIONS(55),
    [anon_sym_WeakenPre] = ACTIONS(55),
    [anon_sym_StrengthenPost] = ACTIONS(55),
    [anon_sym_Var] = ACTIONS(55),
    [anon_sym_Def] = ACTIONS(55),
    [anon_sym_Extract] = ACTIONS(55),
    [anon_sym_Import] = ACTIONS(55),
    [anon_sym_Show] = ACTIONS(55),
    [anon_sym_Eval] = ACTIONS(55),
    [anon_sym_Test] = ACTIONS(55),
    [anon_sym_] = ACTIONS(53),
    [aux_sym_operator_token1] = ACTIONS(53),
    [anon_sym_PLUS] = ACTIONS(53),
    [anon_sym_DASH] = ACTIONS(53),
    [anon_sym_STAR] = ACTIONS(53),
    [anon_sym_2] = ACTIONS(53),
    [aux_sym_operator_token2] = ACTIONS(53),
    [anon_sym_3] = ACTIONS(53),
    [aux_sym_operator_token3] = ACTIONS(53),
    [anon_sym_4] = ACTIONS(53),
    [aux_sym_operator_token4] = ACTIONS(53),
    [anon_sym_5] = ACTIONS(53),
    [aux_sym_operator_token5] = ACTIONS(53),
    [anon_sym_CARET] = ACTIONS(53),
    [aux_sym_operator_token6] = ACTIONS(53),
    [anon_sym_6] = ACTIONS(53),
    [aux_sym_operator_token7] = ACTIONS(53),
    [anon_sym_7] = ACTIONS(53),
    [aux_sym_operator_token8] = ACTIONS(53),
    [sym_identifier] = ACTIONS(55),
    [anon_sym_IQOpt] = ACTIONS(55),
    [anon_sym_QOpt] = ACTIONS(55),
    [anon_sym_QProg] = ACTIONS(55),
  },
  [6] = {
    [ts_builtin_sym_end] = ACTIONS(57),
    [sym_full_stop] = ACTIONS(57),
    [anon_sym_SLASH_SLASH] = ACTIONS(57),
    [anon_sym_SLASH_STAR] = ACTIONS(57),
    [anon_sym_abort] = ACTIONS(59),
    [anon_sym_skip] = ACTIONS(59),
    [anon_sym_assert] = ACTIONS(59),
    [anon_sym_if] = ACTIONS(59),
    [anon_sym_then] = ACTIONS(59),
    [anon_sym_else] = ACTIONS(59),
    [anon_sym_end] = ACTIONS(59),
    [anon_sym_while] = ACTIONS(59),
    [anon_sym_do] = ACTIONS(59),
    [anon_sym_Refine] = ACTIONS(59),
    [anon_sym_End] = ACTIONS(59),
    [anon_sym_Choose] = ACTIONS(59),
    [anon_sym_Step] = ACTIONS(59),
    [anon_sym_Seq] = ACTIONS(59),
    [anon_sym_If] = ACTIONS(59),
    [anon_sym_While] = ACTIONS(59),
    [anon_sym_Inv] = ACTIONS(59),
    [anon_sym_WeakenPre] = ACTIONS(59),
    [anon_sym_StrengthenPost] = ACTIONS(59),
    [anon_sym_Var] = ACTIONS(59),
    [anon_sym_Def] = ACTIONS(59),
    [anon_sym_Extract] = ACTIONS(59),
    [anon_sym_Import] = ACTIONS(59),
    [anon_sym_Show] = ACTIONS(59),
    [anon_sym_Eval] = ACTIONS(59),
    [anon_sym_Test] = ACTIONS(59),
    [anon_sym_] = ACTIONS(57),
    [aux_sym_operator_token1] = ACTIONS(57),
    [anon_sym_PLUS] = ACTIONS(57),
    [anon_sym_DASH] = ACTIONS(57),
    [anon_sym_STAR] = ACTIONS(57),
    [anon_sym_2] = ACTIONS(57),
    [aux_sym_operator_token2] = ACTIONS(57),
    [anon_sym_3] = ACTIONS(57),
    [aux_sym_operator_token3] = ACTIONS(57),
    [anon_sym_4] = ACTIONS(57),
    [aux_sym_operator_token4] = ACTIONS(57),
    [anon_sym_5] = ACTIONS(57),
    [aux_sym_operator_token5] = ACTIONS(57),
    [anon_sym_CARET] = ACTIONS(57),
    [aux_sym_operator_token6] = ACTIONS(57),
    [anon_sym_6] = ACTIONS(57),
    [aux_sym_operator_token7] = ACTIONS(57),
    [anon_sym_7] = ACTIONS(57),
    [aux_sym_operator_token8] = ACTIONS(57),
    [sym_identifier] = ACTIONS(59),
    [anon_sym_IQOpt] = ACTIONS(59),
    [anon_sym_QOpt] = ACTIONS(59),
    [anon_sym_QProg] = ACTIONS(59),
  },
  [7] = {
    [ts_builtin_sym_end] = ACTIONS(61),
    [sym_full_stop] = ACTIONS(61),
    [anon_sym_SLASH_SLASH] = ACTIONS(61),
    [anon_sym_SLASH_STAR] = ACTIONS(61),
    [anon_sym_abort] = ACTIONS(63),
    [anon_sym_skip] = ACTIONS(63),
    [anon_sym_assert] = ACTIONS(63),
    [anon_sym_if] = ACTIONS(63),
    [anon_sym_then] = ACTIONS(63),
    [anon_sym_else] = ACTIONS(63),
    [anon_sym_end] = ACTIONS(63),
    [anon_sym_while] = ACTIONS(63),
    [anon_sym_do] = ACTIONS(63),
    [anon_sym_Refine] = ACTIONS(63),
    [anon_sym_End] = ACTIONS(63),
    [anon_sym_Choose] = ACTIONS(63),
    [anon_sym_Step] = ACTIONS(63),
    [anon_sym_Seq] = ACTIONS(63),
    [anon_sym_If] = ACTIONS(63),
    [anon_sym_While] = ACTIONS(63),
    [anon_sym_Inv] = ACTIONS(63),
    [anon_sym_WeakenPre] = ACTIONS(63),
    [anon_sym_StrengthenPost] = ACTIONS(63),
    [anon_sym_Var] = ACTIONS(63),
    [anon_sym_Def] = ACTIONS(63),
    [anon_sym_Extract] = ACTIONS(63),
    [anon_sym_Import] = ACTIONS(63),
    [anon_sym_Show] = ACTIONS(63),
    [anon_sym_Eval] = ACTIONS(63),
    [anon_sym_Test] = ACTIONS(63),
    [anon_sym_] = ACTIONS(61),
    [aux_sym_operator_token1] = ACTIONS(61),
    [anon_sym_PLUS] = ACTIONS(61),
    [anon_sym_DASH] = ACTIONS(61),
    [anon_sym_STAR] = ACTIONS(61),
    [anon_sym_2] = ACTIONS(61),
    [aux_sym_operator_token2] = ACTIONS(61),
    [anon_sym_3] = ACTIONS(61),
    [aux_sym_operator_token3] = ACTIONS(61),
    [anon_sym_4] = ACTIONS(61),
    [aux_sym_operator_token4] = ACTIONS(61),
    [anon_sym_5] = ACTIONS(61),
    [aux_sym_operator_token5] = ACTIONS(61),
    [anon_sym_CARET] = ACTIONS(61),
    [aux_sym_operator_token6] = ACTIONS(61),
    [anon_sym_6] = ACTIONS(61),
    [aux_sym_operator_token7] = ACTIONS(61),
    [anon_sym_7] = ACTIONS(61),
    [aux_sym_operator_token8] = ACTIONS(61),
    [sym_identifier] = ACTIONS(63),
    [anon_sym_IQOpt] = ACTIONS(63),
    [anon_sym_QOpt] = ACTIONS(63),
    [anon_sym_QProg] = ACTIONS(63),
  },
  [8] = {
    [ts_builtin_sym_end] = ACTIONS(65),
    [sym_full_stop] = ACTIONS(65),
    [anon_sym_SLASH_SLASH] = ACTIONS(65),
    [anon_sym_SLASH_STAR] = ACTIONS(65),
    [anon_sym_abort] = ACTIONS(67),
    [anon_sym_skip] = ACTIONS(67),
    [anon_sym_assert] = ACTIONS(67),
    [anon_sym_if] = ACTIONS(67),
    [anon_sym_then] = ACTIONS(67),
    [anon_sym_else] = ACTIONS(67),
    [anon_sym_end] = ACTIONS(67),
    [anon_sym_while] = ACTIONS(67),
    [anon_sym_do] = ACTIONS(67),
    [anon_sym_Refine] = ACTIONS(67),
    [anon_sym_End] = ACTIONS(67),
    [anon_sym_Choose] = ACTIONS(67),
    [anon_sym_Step] = ACTIONS(67),
    [anon_sym_Seq] = ACTIONS(67),
    [anon_sym_If] = ACTIONS(67),
    [anon_sym_While] = ACTIONS(67),
    [anon_sym_Inv] = ACTIONS(67),
    [anon_sym_WeakenPre] = ACTIONS(67),
    [anon_sym_StrengthenPost] = ACTIONS(67),
    [anon_sym_Var] = ACTIONS(67),
    [anon_sym_Def] = ACTIONS(67),
    [anon_sym_Extract] = ACTIONS(67),
    [anon_sym_Import] = ACTIONS(67),
    [anon_sym_Show] = ACTIONS(67),
    [anon_sym_Eval] = ACTIONS(67),
    [anon_sym_Test] = ACTIONS(67),
    [anon_sym_] = ACTIONS(65),
    [aux_sym_operator_token1] = ACTIONS(65),
    [anon_sym_PLUS] = ACTIONS(65),
    [anon_sym_DASH] = ACTIONS(65),
    [anon_sym_STAR] = ACTIONS(65),
    [anon_sym_2] = ACTIONS(65),
    [aux_sym_operator_token2] = ACTIONS(65),
    [anon_sym_3] = ACTIONS(65),
    [aux_sym_operator_token3] = ACTIONS(65),
    [anon_sym_4] = ACTIONS(65),
    [aux_sym_operator_token4] = ACTIONS(65),
    [anon_sym_5] = ACTIONS(65),
    [aux_sym_operator_token5] = ACTIONS(65),
    [anon_sym_CARET] = ACTIONS(65),
    [aux_sym_operator_token6] = ACTIONS(65),
    [anon_sym_6] = ACTIONS(65),
    [aux_sym_operator_token7] = ACTIONS(65),
    [anon_sym_7] = ACTIONS(65),
    [aux_sym_operator_token8] = ACTIONS(65),
    [sym_identifier] = ACTIONS(67),
    [anon_sym_IQOpt] = ACTIONS(67),
    [anon_sym_QOpt] = ACTIONS(67),
    [anon_sym_QProg] = ACTIONS(67),
  },
  [9] = {
    [ts_builtin_sym_end] = ACTIONS(69),
    [sym_full_stop] = ACTIONS(69),
    [anon_sym_SLASH_SLASH] = ACTIONS(69),
    [anon_sym_SLASH_STAR] = ACTIONS(69),
    [anon_sym_abort] = ACTIONS(71),
    [anon_sym_skip] = ACTIONS(71),
    [anon_sym_assert] = ACTIONS(71),
    [anon_sym_if] = ACTIONS(71),
    [anon_sym_then] = ACTIONS(71),
    [anon_sym_else] = ACTIONS(71),
    [anon_sym_end] = ACTIONS(71),
    [anon_sym_while] = ACTIONS(71),
    [anon_sym_do] = ACTIONS(71),
    [anon_sym_Refine] = ACTIONS(71),
    [anon_sym_End] = ACTIONS(71),
    [anon_sym_Choose] = ACTIONS(71),
    [anon_sym_Step] = ACTIONS(71),
    [anon_sym_Seq] = ACTIONS(71),
    [anon_sym_If] = ACTIONS(71),
    [anon_sym_While] = ACTIONS(71),
    [anon_sym_Inv] = ACTIONS(71),
    [anon_sym_WeakenPre] = ACTIONS(71),
    [anon_sym_StrengthenPost] = ACTIONS(71),
    [anon_sym_Var] = ACTIONS(71),
    [anon_sym_Def] = ACTIONS(71),
    [anon_sym_Extract] = ACTIONS(71),
    [anon_sym_Import] = ACTIONS(71),
    [anon_sym_Show] = ACTIONS(71),
    [anon_sym_Eval] = ACTIONS(71),
    [anon_sym_Test] = ACTIONS(71),
    [anon_sym_] = ACTIONS(69),
    [aux_sym_operator_token1] = ACTIONS(69),
    [anon_sym_PLUS] = ACTIONS(69),
    [anon_sym_DASH] = ACTIONS(69),
    [anon_sym_STAR] = ACTIONS(69),
    [anon_sym_2] = ACTIONS(69),
    [aux_sym_operator_token2] = ACTIONS(69),
    [anon_sym_3] = ACTIONS(69),
    [aux_sym_operator_token3] = ACTIONS(69),
    [anon_sym_4] = ACTIONS(69),
    [aux_sym_operator_token4] = ACTIONS(69),
    [anon_sym_5] = ACTIONS(69),
    [aux_sym_operator_token5] = ACTIONS(69),
    [anon_sym_CARET] = ACTIONS(69),
    [aux_sym_operator_token6] = ACTIONS(69),
    [anon_sym_6] = ACTIONS(69),
    [aux_sym_operator_token7] = ACTIONS(69),
    [anon_sym_7] = ACTIONS(69),
    [aux_sym_operator_token8] = ACTIONS(69),
    [sym_identifier] = ACTIONS(71),
    [anon_sym_IQOpt] = ACTIONS(71),
    [anon_sym_QOpt] = ACTIONS(71),
    [anon_sym_QProg] = ACTIONS(71),
  },
  [10] = {
    [ts_builtin_sym_end] = ACTIONS(73),
    [sym_full_stop] = ACTIONS(73),
    [anon_sym_SLASH_SLASH] = ACTIONS(73),
    [anon_sym_SLASH_STAR] = ACTIONS(73),
    [anon_sym_abort] = ACTIONS(75),
    [anon_sym_skip] = ACTIONS(75),
    [anon_sym_assert] = ACTIONS(75),
    [anon_sym_if] = ACTIONS(75),
    [anon_sym_then] = ACTIONS(75),
    [anon_sym_else] = ACTIONS(75),
    [anon_sym_end] = ACTIONS(75),
    [anon_sym_while] = ACTIONS(75),
    [anon_sym_do] = ACTIONS(75),
    [anon_sym_Refine] = ACTIONS(75),
    [anon_sym_End] = ACTIONS(75),
    [anon_sym_Choose] = ACTIONS(75),
    [anon_sym_Step] = ACTIONS(75),
    [anon_sym_Seq] = ACTIONS(75),
    [anon_sym_If] = ACTIONS(75),
    [anon_sym_While] = ACTIONS(75),
    [anon_sym_Inv] = ACTIONS(75),
    [anon_sym_WeakenPre] = ACTIONS(75),
    [anon_sym_StrengthenPost] = ACTIONS(75),
    [anon_sym_Var] = ACTIONS(75),
    [anon_sym_Def] = ACTIONS(75),
    [anon_sym_Extract] = ACTIONS(75),
    [anon_sym_Import] = ACTIONS(75),
    [anon_sym_Show] = ACTIONS(75),
    [anon_sym_Eval] = ACTIONS(75),
    [anon_sym_Test] = ACTIONS(75),
    [anon_sym_] = ACTIONS(73),
    [aux_sym_operator_token1] = ACTIONS(73),
    [anon_sym_PLUS] = ACTIONS(73),
    [anon_sym_DASH] = ACTIONS(73),
    [anon_sym_STAR] = ACTIONS(73),
    [anon_sym_2] = ACTIONS(73),
    [aux_sym_operator_token2] = ACTIONS(73),
    [anon_sym_3] = ACTIONS(73),
    [aux_sym_operator_token3] = ACTIONS(73),
    [anon_sym_4] = ACTIONS(73),
    [aux_sym_operator_token4] = ACTIONS(73),
    [anon_sym_5] = ACTIONS(73),
    [aux_sym_operator_token5] = ACTIONS(73),
    [anon_sym_CARET] = ACTIONS(73),
    [aux_sym_operator_token6] = ACTIONS(73),
    [anon_sym_6] = ACTIONS(73),
    [aux_sym_operator_token7] = ACTIONS(73),
    [anon_sym_7] = ACTIONS(73),
    [aux_sym_operator_token8] = ACTIONS(73),
    [sym_identifier] = ACTIONS(75),
    [anon_sym_IQOpt] = ACTIONS(75),
    [anon_sym_QOpt] = ACTIONS(75),
    [anon_sym_QProg] = ACTIONS(75),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 1,
    ACTIONS(77), 1,
      aux_sym_line_comment_token1,
  [4] = 1,
    ACTIONS(79), 1,
      aux_sym_block_comment_token1,
  [8] = 1,
    ACTIONS(81), 1,
      ts_builtin_sym_end,
  [12] = 1,
    ACTIONS(83), 1,
      anon_sym_SLASH,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(11)] = 0,
  [SMALL_STATE(12)] = 4,
  [SMALL_STATE(13)] = 8,
  [SMALL_STATE(14)] = 12,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_document, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [11] = {.entry = {.count = 1, .reusable = false}}, SHIFT(5),
  [13] = {.entry = {.count = 1, .reusable = false}}, SHIFT(6),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [17] = {.entry = {.count = 1, .reusable = false}}, SHIFT(4),
  [19] = {.entry = {.count = 1, .reusable = false}}, SHIFT(8),
  [21] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_document, 1),
  [23] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2),
  [25] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(4),
  [28] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(11),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(12),
  [34] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(5),
  [37] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(6),
  [40] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(7),
  [43] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(4),
  [46] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(8),
  [49] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_cmd, 1),
  [51] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_cmd, 1),
  [53] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_prog_keyword, 1),
  [55] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_prog_keyword, 1),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword, 1),
  [59] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword, 1),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1),
  [63] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_operator, 1),
  [65] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_types, 1),
  [67] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_types, 1),
  [69] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_line_comment, 2),
  [71] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_line_comment, 2),
  [73] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block_comment, 3),
  [75] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_block_comment, 3),
  [77] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [79] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [81] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [83] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_rem(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
