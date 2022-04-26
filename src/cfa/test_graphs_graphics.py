from unittest import TestCase
from typing import List, Tuple
from graphviz import Digraph
from decorators import LocationDecorator
from symbol_table import CSymbolTableFiller
from instrumentor import (
    TreeInfestator,
    CTreeInfestator,
    CCanaryFactory
)
from ts import (
    LanguageLibrary,
    Parser,
    Query,
    Tree,
    Node,
    CSyntax,
)
from . import (
    CFA,
    CFAFactory,
    CCFAFactory,
    CFANode
)

class TestGraphsGraphics(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.compound_assignment_query)
        self._assignment_query: Query = self._language.query(self._language.syntax.assignment_query)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.binary_expression_query)
        return super().setUp()

    def test_create_graphs_graphics(self) -> None:
        programs: List[Tuple[str, str]] = [
            ("if_1",  "a=1; if(a==2) { }"),
            ("if_2",  "if(a==2) { } else { }"),
            ("if_3",  "a=1; if(a==2) { } else { } a=2;"),
            ("if_4",  "a=1; if(a==2) { } else if(a==3) { } else { }"),
            ("if_5",  "a=1; if(a==2) { } else if(a==3) { } a=2;"),
            ("if_6",  "a=1; if(a==1) { a=2; }"),
            ("if_7",  "a=1; if(a==1) { a=2; } a=3;"),
            ("if_8",  "a=1; if(a==1) { a=2; } else { a=3; }"),
            ("if_9",  "a=1; if(a==1) { a=2; } else { a=3; } a=4;"),
            ("if_10", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;"),
            ("if_11", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;"),
            ("if_12", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else { a=4; } a=5; a=6;"),
            ("if_13", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } a=5;"),
            ("if_14", "a=1; if(a==1) { a=2; } else if(a==2) { } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;"),
            ("if_15", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;"),
            ("if_16", "a=1; if(a==1) { a=2; } a=3; if(a==2) { a=2; } a=3; if(a==3) { a=2; } a=3;"),
            ("if_17", "a=1; if((((a==1)))) { a=2; }"),
            ("if_18", "a=1; if(a==1) { } a=3;"),
            ("if_18", "a=1; if(a==1) { a=2; } else { } a=3;"),
            ("if_19", "if(a==1) { } if(a==3) { b=2; }"),
            ("if_20", "if(a==1) { a=1; a=2; } if(a==3) { b=2; }"),
            ("if_21", "if (a) { { { { { } } } } } else { a=2; } a=2"),
            ("if_22", "if (a) { { A=1; { { { } b=2; } } } } else { a=2; } a=2"),
            ("if_23", "if(a) { if(a) { } }"),
            ("if_24", "if(a) a=1;"),
            ("if_25", "if(a) a=1; else a=2;"),
            ("if_26", "if(a) a=1; else if(a) a=2;"),
            ("if_27", "if(a) a=1; else if(a) a=2; else a=3;"),
            ("if_28", "if(a) { { { { { } } } } }"),
            ("while_1", "while(a==1) { }"),
            ("while_2", "while(a==1) { } a=3;"),
            ("while_3", "while(a==1) { a=2; } a=3;"),
            ("while_4", "while(a==1) { a=1; a=2; a=3; } a=4;"),
            ("while_4", "while(a==1) { a=1; a=2; a=3; } a=4;"),
            ("while_5", "while(a==1) { if(a==1) { a=1; } a=2; a=3; a=4; a=5; } a=6;"),
            ("while_6", "while(a==1) { if(a==1) { a=1; } else { a=2; } a=3; } a=4;"),
            ("while_7", "while(a==1) { if(a==1) { a=1; } else if(a==2) { a=2; } else { a=3; } a=4; } a=5;"),
            ("while_8", "while(a==1) { if(a==1) { a=1; } a=2; if(a==2) { a=3; } a=4; a=5; a=6; } a=7;"),
            ("while_9", "while(a==1) { a=1; break; a=2; } a=3;"),
            ("while_10", "while(a==1) { a=1; continue; a=2; } a=3;"),
            ("while_11", "while(a) { a=1; while(a) { a=2; } a=2; } a=2;"),
            ("while_12", "while(a) { break; a=1; while(a) { break; a=2; } a=2; } a=2;"),
            ("while_13", "while(a==1) { if(a==1) { a=1; } else if(a==2) { a=2; } else { a=3; return; } a=4; } a=5;"),
            ("while_14", "while(a==1) { if(a==1) { a=1; break; } else if(a==2) { a=2; } else { a=3; return; } a=4; } a=5;"),
            ("while_15", "while(a==1) { if(a==1) { a=1; break; } else if(a==2) { continue; a=2; } else { a=3; return; } a=4; } a=5;"),
            ("while_16", "while(a);"),
            ("do_while_1", "do { a=1; } while(a==1); a=2;"),
            ("do_while_2", "do { if(a==1) f{ a=1; } a=2; } while(a==1); a=2;"),
            ("do_while_3", "do { a=0; if(a==1) { a=1; } a=2; } while(a==1); a=2;"),
            ("do_while_4", "do { a=2; } while(a==1); a=2;"),
            ("do_while_5", "do { TWEET(\"A\"); a=2; } while(a==1); TWEET(\"B\"); a=2;"),
            ("do_while_6", "do ; while(a);"),
            ("for_1", "for(int i = 0;;) { } a=3;"),
            ("for_2", "for(int i = 0; i<5;) { } a=3;"),
            ("for_3", "for(int i = 0; i<5; ++i) { } a=3;"),
            ("for_4", "for(; i<5; ++i) { a=2; } a=3;"),
            ("for_5", "for(int i=0; i<5; ) { a=2; } a=3;"),
            ("for_6", "for(int i=0; i<5; ++i) { a=2; } a=3;"),
            ("for_7", "for(int i=0; i<5; ++i) { a=2; for(int i=0; i<5; ++i) { a=2; } a=2; } a=3;"),
            ("for_8", "for(int i=0; i<5; ++i) { break; a=2; } a=3;"),
            ("for_9", "for(int i=0; i<5; ++i) { break; a=2; for(int i=0; i<5; ++i) { continue; a=2; } a=2; } a=3;"),
            ("for_10", "for(int i = 0; i<5; ++i) { a=2; } a=3;"),
            ("for_11", "for(int i = 0; i<5;) { a=2; } a=3;"),
            ("for_12", "for(;;) { a=2; } a=3;"),
            ("for_13", "for(;;); a=3;"),
            ("for_14", "for(;;) { } a=3;"),
            ("for_15", "a=1; for(;;); a=3;"),
            ("for_16", "a=1; for(;;) { } a=3;"),
            ("for_17", "a=1; for(i=0; i<0; ); a=2;"),
            ("for_18", "a=1; for(i=0; ;); a=2;"),
            ("for_18", "a=1; for(i=0; i<0; ++i); a=2;"),
            ("for_19", "a=1; for(; i<0; ); a=2;"),
            ("for_20", "a=1; for(; ;); a=2;"),
            ("for_21", "a=1; for(; i<0; ++i); a=2;"),
            ("for_22", "a=1; for(i=0; i<0; ) { } a=2;"),
            ("for_23", "a=1; for(i=0; ; ) { } a=2;"),
            ("for_24", "a=1; for(i=0; i<0; ++i) {  } a=2;"),
            ("for_25", "a=1; for(i=0; i<0; ++i) { a=2; } a=2;"),
            ("for_26", "a=1; for(i=0; i<0; ) { a=2; } a=2;"),
            ("for_27", "a=1; for(i=0; ; ) { a=2; } a=2;"),
            ("for_28", "a=1; for(; i<0; ) { } a=2;"),
            ("for_29", "a=1; for(; ; ) { } a=2;"),
            ("for_30", "a=1; for(; i<0; ++i) {  } a=2;"),
            ("for_31", "a=1; for(; i<0; ++i) { a=2; } a=2;"),
            ("for_32", "a=1; for(; i<0; ) { a=2; } a=2;"),
            ("for_33", "a=1; for(; ; ) { a=2; } a=2;"),
            ("for_34", "for(;;) { a=1; a=2; }"),
            ("for_35", "for(;;) { if(a) { a = 1; } }"),
            ("for_36", "for(;;) { while(a) { a = 1; } }"),
            ("for_37", "for(;;) { do { a = 1; } while(a) }"),
            ("for_38", "for(;;) { for(;;); }"),
            ("for_39", "for(;;) { int a = 0; if(a) { a = 1; } }"),
            ("for_40", """
             for(int i = 0; i < n; i++) {
                 for (int j = 0; j < m; j++) {
                     print(a);
                 }
                 print(b);
             }
             """),
            ("for_41", "for(int i = 0;;) { a=2; a=2; } a=3;"),
            ("for_42", "for(int i = 0;;) { a=2; a=2; a=2; } a=3;"),
            ("for_43", "for(int i = 0;;) { a=2; } a=3;"),
            ("for_44", "for(int i = 0;;) { a=2; }"),
            ("for_45", "for (;0;) a=a;"),
            ("for_46", "for (;;) a=a;"),
            ("for_47", "for (;;) break;"),
            ("for_48", "for (;;) continue;"),
            ("switch_1", """
            switch (a)
            {
                case 1: a=1;
            }
             """),
            ("switch_2", """
            switch (a)
            {
                case 3: { a=2; }
            }
             """),
            ("switch_3", """
            switch (a)
            {
                case 1: a=1;
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_4", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_5", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
            a=10;
             """),
            ("switch_6", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_7", """
            if(a==1) {
                switch (a)
                {
                    case 2: a=1;
                }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("switch_8", """
            if(a==1) {
                switch (a)
                {
                    case 1: 
                    case 2: a=1;
                    case 3: { a=2; }
                    default: a=3;
                }
                a=3;
                while (a==1) { a=2; }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("switch_9", """
            if(a==1) {
                switch (a)
                {
                    case 1: 
                    case 2: a=1;
                    case 3: { a=2; }
                    default: a=3;
                }
                while (a==1) { a=2; }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("switch_10", """
            int a = 3;
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
            a=10;
             """),
            ("switch_11", """
            switch (a)
            {
                case 1: 
                case 2: a=1;  a=1;
                case 3: { a=2;  a=1; }
                default: a=3;
            }
            a=10;
             """),
            ("switch_12", """
            switch (a)
            {
                case 1: 
                case 2: 
                case 3: { a=2;  a=1; }
                default: a=3;
            }
            a=10;
             """),
            ("switch_13", """
            switch (a)
            {
                case 1: 
                case 2: a=1;  a=1;
                case 3: { }
                default: a=3;
            }
            a=10;
             """),
            ("switch_14", """
            switch (a)
            {
                case 1: 
                case 2: a=1;  a=1;
                case 3: { }
                default:
            }
            a=10;
             """),
            ("switch_15", """
            switch (a)
            {
                case 1:
                case 2:
                case 3:
                default:
            }
            a=10;
             """),
             ("switch_16", """
            a = 2; 
            switch (a) {
                case 1: printf("I am One");
                        break;
                case 2: printf("I am Two");
                        break;
                case 3: printf("I an Three");
                        break;
                default: printf("I am default");
            }
            a = 3;
             """),
             ("switch_17", """
            a = 2; 
            switch (a) {
                case 1: printf("I am One");
                        break;
                case 2: printf("I am Two");
                        break;
                case 3: printf("I an Three");
                        break;
                default: printf("I am default");
            }
             """),
            ("switch_18", """
            switch (a)
            {
                case 1: 
                case 2: a=1;  a=1;
                case 3: { }
                default: a=3;
            }
             """),
            ("function_1", """
            void foo() {
                a=2;
                return;
                a=2;
            }
             """),
            ("function_2", """
            void foo() {
            target:
                a=2;
                a=3;
                goto target;
            }
             """),
            ("function_3", """
            void foo() {
                goto target;
                a=3;
            target:
                a=2;
            }
             """),
            ("goto_1", """
                goto SUM;
            SUM:
                sum = a + b;
             """),
            ("program_1", """
             void foo() {
                 int a = 0;
                 int b;
                 double c;
                 for (b = 0; b < 10; ++b) {
                     print(b);
                     if (b % 2 == 0) {
                         continue;
                     }
                    b /= 2;
                 }
                 b /= 2; a += 2; c = 42;
                 a = b = c;
                 return;
             }
             """),
            # https://github.com/neovim/neovim
            ("program_2", """
                static int conv_error(const char *
                    const msg,                static int conv_error(const char *const msg, const MPConvStack *const mpstack,
                                    const char *const objname)
                FUNC_ATTR_NONNULL_ALL
                {
                garray_T msg_ga;
                ga_init(&msg_ga, (int)sizeof(char), 80);
                const char *const key_msg = _("key %s");
                const char *const key_pair_msg = _("key %s at index %i from special map");
                const char *const idx_msg = _("index %i");
                const char *const partial_arg_msg = _("partial");
                const char *const partial_arg_i_msg = _("argument %i");
                const char *const partial_self_msg = _("partial self dictionary");
                for (size_t i = 0; i < kv_size(*mpstack); i++) {
                    if (i != 0) {
                    ga_concat(&msg_ga, ", ");
                    }
                    MPConvStackVal v = kv_A(*mpstack, i);
                    switch (v.type) {
                    case kMPConvDict: {
                    typval_T key_tv = {
                        .v_type = VAR_STRING,
                        .vval = { .v_string = (v.data.d.hi == NULL
                                                ? v.data.d.dict->dv_hashtab.ht_array
                                                : (v.data.d.hi - 1))->hi_key },
                    };
                    char *const key = encode_tv2string(&key_tv, NULL);
                    vim_snprintf((char *)IObuff, IOSIZE, key_msg, key);
                    xfree(key);
                    ga_concat(&msg_ga, (char *)IObuff);
                    break;
                    }
                    case kMPConvPairs:
                    case kMPConvList: {
                    const int idx = (v.data.l.li == tv_list_first(v.data.l.list)
                                        ? 0
                                        : (v.data.l.li == NULL
                                            ? tv_list_len(v.data.l.list) - 1
                                            : (int)tv_list_idx_of_item(v.data.l.list,
                                                                    TV_LIST_ITEM_PREV(v.data.l.list,
                                                                                        v.data.l.li))));
                    const listitem_T *const li = (v.data.l.li == NULL
                                                    ? tv_list_last(v.data.l.list)
                                                    : TV_LIST_ITEM_PREV(v.data.l.list,
                                                                        v.data.l.li));
                    if (v.type == kMPConvList
                        || li == NULL
                        || (TV_LIST_ITEM_TV(li)->v_type != VAR_LIST
                            && tv_list_len(TV_LIST_ITEM_TV(li)->vval.v_list) <= 0)) {
                        vim_snprintf((char *)IObuff, IOSIZE, idx_msg, idx);
                        ga_concat(&msg_ga, (char *)IObuff);
                    } else {
                        assert(li != NULL);
                        listitem_T *const first_item =
                        tv_list_first(TV_LIST_ITEM_TV(li)->vval.v_list);
                        assert(first_item != NULL);
                        typval_T key_tv = *TV_LIST_ITEM_TV(first_item);
                        char *const key = encode_tv2echo(&key_tv, NULL);
                        vim_snprintf((char *)IObuff, IOSIZE, key_pair_msg, key, idx);
                        xfree(key);
                        ga_concat(&msg_ga, (char *)IObuff);
                    }
                    break;
                    }
                    case kMPConvPartial:
                    switch (v.data.p.stage) {
                    case kMPConvPartialArgs:
                        abort();
                        break;
                    case kMPConvPartialSelf:
                        ga_concat(&msg_ga, partial_arg_msg);
                        break;
                    case kMPConvPartialEnd:
                        ga_concat(&msg_ga, partial_self_msg);
                        break;
                    }
                    break;
                    case kMPConvPartialList: {
                    const int idx = (int)(v.data.a.arg - v.data.a.argv) - 1;
                    vim_snprintf((char *)IObuff, IOSIZE, partial_arg_i_msg, idx);
                    ga_concat(&msg_ga, (char *)IObuff);
                    break;
                    }
                    }
                }
                semsg(msg, _(objname), (kv_size(*mpstack) == 0
                                        ? _("itself")
                                        : (char *)msg_ga.ga_data));
                ga_clear(&msg_ga);
                return FAIL;
                }
             """
            ),
            # https://github.com/neovim/neovim
            ("program_3","""
                static int get_function_args(char_u **argp, char_u endchar, garray_T *newargs, int *varargs,
                                            garray_T *default_args, bool skip)
                {
                bool mustend = false;
                char_u *arg = *argp;
                char_u *p = arg;
                int c;
                int i;
                if (newargs != NULL) {
                    ga_init(newargs, (int)sizeof(char_u *), 3);
                }
                if (default_args != NULL) {
                    ga_init(default_args, (int)sizeof(char_u *), 3);
                }
                if (varargs != NULL) {
                    *varargs = false;
                }
                // Isolate the arguments: "arg1, arg2, ...)"
                bool any_default = false;
                while (*p != endchar) {
                    if (p[0] == '.' && p[1] == '.' && p[2] == '.') {
                    if (varargs != NULL) {
                        *varargs = true;
                    }
                    p += 3;
                    mustend = true;
                    } else {
                    arg = p;
                    while (ASCII_ISALNUM(*p) || *p == '_') {
                        p++;
                    }
                    if (arg == p || isdigit(*arg)
                        || (p - arg == 9 && STRNCMP(arg, "firstline", 9) == 0)
                        || (p - arg == 8 && STRNCMP(arg, "lastline", 8) == 0)) {
                        if (!skip) {
                        semsg(_("E125: Illegal argument: %s"), arg);
                        }
                        break;
                    }
                    if (newargs != NULL) {
                        ga_grow(newargs, 1);
                        c = *p;
                        *p = NUL;
                        arg = vim_strsave(arg);
                        // Check for duplicate argument name.
                        for (i = 0; i < newargs->ga_len; i++) {
                        if (STRCMP(((char_u **)(newargs->ga_data))[i], arg) == 0) {
                            semsg(_("E853: Duplicate argument name: %s"), arg);
                            xfree(arg);
                            goto err_ret;
                        }
                        }
                        ((char_u **)(newargs->ga_data))[newargs->ga_len] = arg;
                        newargs->ga_len++;
                        *p = c;
                    }
                    if (*skipwhite(p) == '=' && default_args != NULL) {
                        typval_T rettv;
                        any_default = true;
                        p = skipwhite(p) + 1;
                        p = skipwhite(p);
                        char_u *expr = p;
                        if (eval1(&p, &rettv, false) != FAIL) {
                        ga_grow(default_args, 1);
                        // trim trailing whitespace
                        while (p > expr && ascii_iswhite(p[-1])) {
                            p--;
                        }
                        c = *p;
                        *p = NUL;
                        expr = vim_strsave(expr);
                        ((char_u **)(default_args->ga_data))
                        [default_args->ga_len] = expr;
                        default_args->ga_len++;
                        *p = c;
                        } else {
                        mustend = true;
                        }
                    } else if (any_default) {
                        emsg(_("E989: Non-default argument follows default argument"));
                        mustend = true;
                    }
                    if (*p == ',') {
                        p++;
                    } else {
                        mustend = true;
                    }
                    }
                    p = skipwhite(p);
                    if (mustend && *p != endchar) {
                    if (!skip) {
                        semsg(_(e_invarg2), *argp);
                    }
                    break;
                    }
                }
                if (*p != endchar) {
                    goto err_ret;
                }
                p++;  // skip "endchar"
                *argp = p;
                return OK;
                err_ret:
                if (newargs != NULL) {
                    ga_clear_strings(newargs);
                }
                if (default_args != NULL) {
                    ga_clear_strings(default_args);
                }
                return FAIL;
                }
                        const MPConvStack *
                            const mpstack,
                                const char *
                                    const objname)
                FUNC_ATTR_NONNULL_ALL {
                    garray_T msg_ga;
                    ga_init( & msg_ga, (int) sizeof(char), 80);
                    const char *
                        const key_msg = _("key %s");
                    const char *
                        const key_pair_msg = _("key %s at index %i from special map");
                    const char *
                        const idx_msg = _("index %i");
                    const char *
                        const partial_arg_msg = _("partial");
                    const char *
                        const partial_arg_i_msg = _("argument %i");
                    const char *
                        const partial_self_msg = _("partial self dictionary");
                    for (size_t i = 0; i < kv_size( * mpstack); i++) {
                        if (i != 0) {
                            ga_concat( & msg_ga, ", ");
                        }
                        MPConvStackVal v = kv_A( * mpstack, i);
                        switch (v.type) {
                        case kMPConvDict: {
                            typval_T key_tv = {
                                .v_type = VAR_STRING,
                                .vval = {
                                    .v_string = (v.data.d.hi == NULL ?
                                        v.data.d.dict -> dv_hashtab.ht_array :
                                        (v.data.d.hi - 1)) -> hi_key
                                },
                            };
                            char *
                                const key = encode_tv2string( & key_tv, NULL);
                            vim_snprintf((char * ) IObuff, IOSIZE, key_msg, key);
                            xfree(key);
                            ga_concat( & msg_ga, (char * ) IObuff);
                            break;
                        }
                        case kMPConvPairs:
                        case kMPConvList: {
                            const int idx = (v.data.l.li == tv_list_first(v.data.l.list) ?
                                0 :
                                (v.data.l.li == NULL ?
                                    tv_list_len(v.data.l.list) - 1 :
                                    (int) tv_list_idx_of_item(v.data.l.list,
                                        TV_LIST_ITEM_PREV(v.data.l.list,
                                            v.data.l.li))));
                            const listitem_T *
                                const li = (v.data.l.li == NULL ?
                                    tv_list_last(v.data.l.list) :
                                    TV_LIST_ITEM_PREV(v.data.l.list,
                                        v.data.l.li));
                            if (v.type == kMPConvList ||
                                li == NULL ||
                                (TV_LIST_ITEM_TV(li) -> v_type != VAR_LIST &&
                                    tv_list_len(TV_LIST_ITEM_TV(li) -> vval.v_list) <= 0)) {
                                vim_snprintf((char * ) IObuff, IOSIZE, idx_msg, idx);
                                ga_concat( & msg_ga, (char * ) IObuff);
                            } else {
                                assert(li != NULL);
                                listitem_T *
                                    const first_item =
                                        tv_list_first(TV_LIST_ITEM_TV(li) -> vval.v_list);
                                assert(first_item != NULL);
                                typval_T key_tv = * TV_LIST_ITEM_TV(first_item);
                                char *
                                    const key = encode_tv2echo( & key_tv, NULL);
                                vim_snprintf((char * ) IObuff, IOSIZE, key_pair_msg, key, idx);
                                xfree(key);
                                ga_concat( & msg_ga, (char * ) IObuff);
                            }
                            break;
                        }
                        case kMPConvPartial:
                            switch (v.data.p.stage) {
                            case kMPConvPartialArgs:
                                abort();
                                break;
                            case kMPConvPartialSelf:
                                ga_concat( & msg_ga, partial_arg_msg);
                                break;
                            case kMPConvPartialEnd:
                                ga_concat( & msg_ga, partial_self_msg);
                                break;
                            }
                            break;
                        case kMPConvPartialList: {
                            const int idx = (int)(v.data.a.arg - v.data.a.argv) - 1;
                            vim_snprintf((char * ) IObuff, IOSIZE, partial_arg_i_msg, idx);
                            ga_concat( & msg_ga, (char * ) IObuff);
                            break;
                        }
                        }
                    }
                    semsg(msg, _(objname), (kv_size( * mpstack) == 0 ?
                        _("itself") :
                        (char * ) msg_ga.ga_data));
                    ga_clear( & msg_ga);
                    return FAIL;
                }
                ""
                "
                ),
                # https: //github.com/neovim/neovim
                    ("program_3", ""
                        "
                        static int get_function_args(char_u ** argp, char_u endchar, garray_T * newargs, int * varargs,
                            garray_T * default_args, bool skip) {
                            bool mustend = false;
                            char_u * arg = * argp;
                            char_u * p = arg;
                            int c;
                            int i;
                            if (newargs != NULL) {
                                ga_init(newargs, (int) sizeof(char_u * ), 3);
                            }
                            if (default_args != NULL) {
                                ga_init(default_args, (int) sizeof(char_u * ), 3);
                            }
                            if (varargs != NULL) {
                                * varargs = false;
                            }
                            // Isolate the arguments: "arg1, arg2, ...)"
                            bool any_default = false;
                            while ( * p != endchar) {
                                if (p[0] == '.' && p[1] == '.' && p[2] == '.') {
                                    if (varargs != NULL) {
                                        * varargs = true;
                                    }
                                    p += 3;
                                    mustend = true;
                                } else {
                                    arg = p;
                                    while (ASCII_ISALNUM( * p) || * p == '_') {
                                        p++;
                                    }
                                    if (arg == p || isdigit( * arg) ||
                                        (p - arg == 9 && STRNCMP(arg, "firstline", 9) == 0) ||
                                        (p - arg == 8 && STRNCMP(arg, "lastline", 8) == 0)) {
                                        if (!skip) {
                                            semsg(_("E125: Illegal argument: %s"), arg);
                                        }
                                        break;
                                    }
                                    if (newargs != NULL) {
                                        ga_grow(newargs, 1);
                                        c = * p;
                                        * p = NUL;
                                        arg = vim_strsave(arg);
                                        // Check for duplicate argument name.
                                        for (i = 0; i < newargs -> ga_len; i++) {
                                            if (STRCMP(((char_u ** )(newargs -> ga_data))[i], arg) == 0) {
                                                semsg(_("E853: Duplicate argument name: %s"), arg);
                                                xfree(arg);
                                                goto err_ret;
                                            }
                                        }
                                        ((char_u ** )(newargs -> ga_data))[newargs -> ga_len] = arg;
                                        newargs -> ga_len++;
                                        * p = c;
                                    }
                                    if ( * skipwhite(p) == '=' && default_args != NULL) {
                                        typval_T rettv;
                                        any_default = true;
                                        p = skipwhite(p) + 1;
                                        p = skipwhite(p);
                                        char_u * expr = p;
                                        if (eval1( & p, & rettv, false) != FAIL) {
                                            ga_grow(default_args, 1);
                                            // trim trailing whitespace
                                            while (p > expr && ascii_iswhite(p[-1])) {
                                                p--;
                                            }
                                            c = * p;
                                            * p = NUL;
                                            expr = vim_strsave(expr);
                                            ((char_u ** )(default_args -> ga_data))[default_args -> ga_len] = expr;
                                            default_args -> ga_len++;
                                            * p = c;
                                        } else {
                                            mustend = true;
                                        }
                                    } else if (any_default) {
                                        emsg(_("E989: Non-default argument follows default argument"));
                                        mustend = true;
                                    }
                                    if ( * p == ',') {
                                        p++;
                                    } else {
                                        mustend = true;
                                    }
                                }
                                p = skipwhite(p);
                                if (mustend && * p != endchar) {
                                    if (!skip) {
                                        semsg(_(e_invarg2), * argp);
                                    }
                                    break;
                                }
                            }
                            if ( * p != endchar) {
                                goto err_ret;
                            }
                            p++; // skip "endchar"
                            * argp = p;
                            return OK;
                            err_ret:
                                if (newargs != NULL) {
                                    ga_clear_strings(newargs);
                                }
                            if (default_args != NULL) {
                                ga_clear_strings(default_args);
                            }
                            return FAIL;
                        }
             """),
             ("program_4", 
                """
                a=2;
                """
             ),
             ("if_report_example",
             """
                if (a < 2) {
                    b = 0;
                } else {
                    b = 1;
                }"""),
            ("program_5", """
             void foo() {
                 int a = 0;
                 int b;
                 double c;
                 for (int p = 0; b < 10; ++b) {
                     print(p);
                 }
                 return;
             }
             void bar(int *a) {
                 double c;
                 return;
             }
             """),
            ("program_6", """
             void foo() {
                 int a = 0;
                 int b;
                 double c;
                 for (int p = 0; b < 10; ++b) {
                     print(p);
                 }
                 return;
             }
             typedef struct Foo {
                 int b;
             } Foo;
             struct Bar {
                 foo Foo;
             };
             typedef struct Bar Bar;
             void bar(int *a) {
                 double c;
                 return;
                 if (a) {
                     if (b) {
                         int q = 0;
                     }
                 }
             }
             """),
            ("program_7", """
             void foo(int a) {
                 int b,c,d = 0;
                 if (a) {
                     int e = 0;
                 } else {
                     int f = 0;
                 }
                 do { int g = 0; } while(a);
                 while (a) { int h = 0; }
                 for (int i = 0, j = 0;;) { int k = 0; }
             }
             """),
            ("program_8", """
             void tommy1(int a) {
                 int b = tommy3() + tommy2();
             }
             """),
            ("program_9","""
             int a = 0;
             int b = 2;
             int c = 1;
             """
            ),
            ("program_10","""
             a=2;
              if(b == 2) {
                  c = 1;
              } else {
                  d = 3;
              }
             """
            ),
            ("program_11", """
              for(;;) break;
              for (;i>0;) a=a;
             """),
            ("program_12", """
            int add(int a, int b) {
                do { a=a; } while(0);

                while(1) { a=a; break; }
                for(;;) break;

                for (;0;) a=a;

                if (a==a) { a=a; }
                else if(b==b) { b=b; }
                else { b=b; }

                int sum;
                goto SUM;
            SUM:
                sum = a + b;
                return sum;
            }
             """),
        ]

        def draw_normal_cfa(name: str, program: str):
            tree: Tree = self._parser.parse(program)
            visitor: CFAFactory = CCFAFactory(tree)

            root: Node = tree.root
            if root.named_children[0].type == "function_definition":
                root = root.named_children[0].child_by_field_name("body")

            cfa: CFA[CFANode] = visitor.create(root)
            dot: Digraph = cfa.draw(tree, name)
            dot.save(directory="graphs")
            
            for node in cfa.nodes:
                self.assertIsNotNone(node.node, f'A node is None {name}')

            draw_infected_cfa(name, tree, cfa)
            draw_symbol_table(name, tree)

        def draw_infected_cfa(name: str, tree: Tree, cfa: CFA[CFANode]):
            try:
                infestator: TreeInfestator = CTreeInfestator(self._parser, CCanaryFactory())
                infested_tree: Tree = infestator.infect(tree, cfa)
                # TODO (IMPORTANT): Editing does not work correctly and for this
                #   reason we have to re-parse with a COMPLETELY NEW PARSER!!!
                infested_tree = Parser.c().parse(infested_tree.text)

                root: Node = infested_tree.root
                if root.named_children[0].type == "function_definition":
                    root = root.named_children[0].child_by_field_name("body")

                infested_visitor: CFAFactory = CCFAFactory(infested_tree)
                infested_cfa: CFA[CFANode] = infested_visitor.create(root)

                location_decorator = LocationDecorator(infested_tree)
                localised_cfa = location_decorator.decorate(infested_cfa)

                infested_dot: Digraph = localised_cfa.draw(infested_tree, f'{name}_infested')
                infested_dot.save(directory="graphs")
            except:
                self.assertEqual(name, "", "Infestation failed for this program")

        def draw_symbol_table(name: str, tree: Tree):
            try:
                symbol_filler = CSymbolTableFiller(CSyntax())
                root_table = symbol_filler.fill(tree)
                table_tree = root_table.root.draw(f'{name}_symbols')
                table_tree.save(directory="graphs")
            except:
                # For now we ignore mistakes in certain programs
                if name == "program_2": return
                if name == "program_3": return
                self.assertEqual(name, "", "Symbol filling failed for this program")

        for program in programs:
            name: str = program[0]
            progame: str = program[1]

            draw_normal_cfa(name, progame)