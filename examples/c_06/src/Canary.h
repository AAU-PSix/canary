#include <stdio.h>

#define CANARY_STR_IMPL_(x) #x
#define CANARY_STR(x) CANARY_STR_IMPL_(x)

#define CANARY_IS_INDEXABLE(arg) (sizeof(arg[0]))
#define CANARY_IS_ARRAY(arg) (IS_INDEXABLE(arg) && \
    (((void *) &arg) == ((void *) arg)))

#define CANARY_PRIMITIVE_DEFAULT                (0)
/* CHAR */
#define CANARY_PRIMITIVE_CHAR                   (1)
#define CANARY_PRIMITIVE_SIGNED_CHAR            (2)
#define CANARY_PRIMITIVE_UNSIGNED_CHAR          (3)
/* SHORT */
#define CANARY_PRIMITIVE_SHORT                  (4)
#define CANARY_PRIMITIVE_SHORT_INT              (5)
#define CANARY_PRIMITIVE_SIGNED_SHORT           (6)
#define CANARY_PRIMITIVE_SIGNED_SHORT_INT       (7)
#define CANARY_PRIMITIVE_UNSIGNED_SHORT         (8)
#define CANARY_PRIMITIVE_UNSIGNED_SHORT_INT     (9)
/* INT */
#define CANARY_PRIMITIVE_INT                    (10)
#define CANARY_PRIMITIVE_SIGNED                 (11)
#define CANARY_PRIMITIVE_SIGNED_INT             (12)
#define CANARY_PRIMITIVE_UNSIGNED               (13)
#define CANARY_PRIMITIVE_UNSIGNED_INT           (14)
/* LONG */
#define CANARY_PRIMITIVE_LONG                   (15)
#define CANARY_PRIMITIVE_LONG_INT               (16)
#define CANARY_PRIMITIVE_SIGNED_LONG            (17)
#define CANARY_PRIMITIVE_SIGNED_LONG_INT        (18)
/* LONG LONG */
#define CANARY_PRIMITIVE_LONG_LONG              (19)
#define CANARY_PRIMITIVE_LONG_LONG_INT          (20)
#define CANARY_PRIMITIVE_SIGNED_LONG_LONG       (21)
#define CANARY_PRIMITIVE_SIGNED_LONG_LONG_INT   (22)
#define CANARY_PRIMITIVE_UNSIGNED_LONG_LONG     (23)
#define CANARY_PRIMITIVE_UNSIGNED_LONG_LONG_INT (24)
/* FLOAT */
#define CANARY_PRIMITIVE_FLOAT                  (25)
/* DOUBLE */
#define CANARY_PRIMITIVE_DOUBLE                 (26)
/* LONG DOUBLE */
#define CANARY_PRIMITIVE_LONG_DOUBLE            (27)

#define CANARY_TYPECHECK(T)             \
(_Generic( (T),                         \
    char: CANARY_PRIMITIVE_CHAR,        \
    int: CANARY_PRIMITIVE_INT,          \
    long: CANARY_PRIMITIVE_LONG,        \
    float: CANARY_PRIMITIVE_FLOAT,      \
    default: CANARY_PRIMITIVE_DEFAULT   \
))

#define CANARY_INT_FORMAT "%d"
#define CANARY_FLOAT_FORMAT "%f"
#define CANARY_DOUBLE_FORMAT "%lf"
#define CANARY_LL_FORMAT "%lld"

#define CANARY_TWEET_LOCATION(l)\
do {                            \
    printf("location="l"\n");   \
} while(0)


#define CANARY_TWEET_PRIMITIVE(VAR)                         \
do {                                                        \
    switch (CANARY_TYPECHECK(VAR)) {                        \
        case CANARY_PRIMITIVE_INT:                          \
            CANARY_TWEET_VARIABLE(VAR, CANARY_INT_FORMAT);  \
            break;                                          \
    }                                                       \
} while(0)

#define CANARY_TWEET_VARIABLE(VAR, FORMAT)          \
    CANARY_TWEET_STATE(CANARY_STR(VAR), VAR, FORMAT)

#define CANARY_TWEET_STATE(ID, VAL, FORMAT) \
do {                                        \
    printf("state="ID"\n");                 \
    printf("value="FORMAT"\n", VAL);        \
} while(0)