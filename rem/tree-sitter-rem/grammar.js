module.exports = grammar({
    name: "rem",
    // 跳过空白符号
    extras: () => [
        /\s/
    ],
    rules: {
        document: $ => repeat($.cmd),

        cmd: $ => choice(
            $.line_comment,
            $.block_comment,

            $.prog_keyword,
            $.keyword,
            $.operator,
            $.identifier,
            $.types,

            $.full_stop,
        ),

        full_stop: $ => '.',

        line_comment: $ => seq('//', /.*/),

        block_comment: $ => seq('/*', /[^*]*\*+([^/*][^*]*\*+)*/, '/'),

        prog_keyword: $ => choice(
            'abort',
            'skip',
            'assert',
            'if',
            'then',
            'else',
            'end',
            'while',
            'do',
        ),

        keyword: $ => choice(
            'Refine',
            'End',
            'Choose',

            'Step',
            'Seq',
            'If',
            'While',
            'Inv',

            'WeakenPre',
            'StrengthenPost',
            
            'Var',
            'Def',
            
            'Extract',
            'Import',

            'Show',
            'Eval',
            'Test',
        ),


        operator: $ => prec(2, choice(
            '⊕',
            /\\oplus/,

            '+',
            '-',
            '*',

            '⊗',
            /\\otimes/,

            '†',
            /\^\\dagger/,

            '∨',
            /\\vee/,

            '∧',
            /\\wedge/,

            '^⊥',
            /\^\\perp/,

            '⇝',
            /\\SasakiImply/,

            '⋒',
            /\\SasakiConjunct/,
        )),

        identifier: $ => /[a-zA-Z\'][a-zA-Z\'0-9]*/,

        types: $ => choice(
            'IQOpt',
            'QOpt',
            'QProg',
        ),

    }
});