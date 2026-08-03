---
title: "Functions for data types"
url: "https://ydb.tech/docs/en/yql/reference/builtins/types?version=v26.1"
doc_path: "en/yql/reference/builtins/types"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/builtins/types.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/builtins/types.md"
description: "FormatType."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Functions for data types

## FormatType

Serializing a type or a handle type to a human-readable string. This helps at debugging and will also be used in the next examples of this section. [Documentation for the format](../types/type_string.md).

## ParseType

Building a type from a string with description. [Documentation for its format](../types/type_string.md).

### Examples

```yql
SELECT FormatType(ParseType("List<Int32>"));  -- List<int32>
```

## TypeOf

Getting the type of value passed to the argument.

### Examples {#examples1}

```yql
SELECT FormatType(TypeOf("foo"));  -- String
```

```yql
SELECT FormatType(TypeOf(AsTuple(1, 1u))); -- Tuple<Int32,Uint32>
```

## InstanceOf

Returns an instance of the specified type that can only be used to get the type of the result of an expression that uses this type.

If this instance remains in the computation graph by the end of optimization, the operation fails.

### Examples {#examples2}

```yql
SELECT FormatType(TypeOf(
    InstanceOf(ParseType("Int32")) +
    InstanceOf(ParseType("Double"))
)); -- Double, because "Int32 + Double" returns Double
```

## DataType

Returns a type for [primitive data types](../types/primitive.md) based on type name.

### Examples {#examples3}

```yql
SELECT FormatType(DataType("Bool")); -- Bool
SELECT FormatType(DataType("Decimal","5","1")); -- Decimal(5,1)
```

## OptionalType

Adds the option to assign `NULL` to the passed type.

### Examples {#examples4}

```yql
SELECT FormatType(OptionalType(DataType("Bool"))); -- Bool?
```

## ListType and StreamType {#listtype}

Builds a list type or stream type based on the passed element type.

### Examples {#examples5}

```yql
SELECT FormatType(ListType(DataType("Bool"))); -- List<Bool>
```

## DictType

Builds a dictionary type based on the passed key types (first argument) and value types (second argument).

### Examples {#examples6}

```yql
SELECT FormatType(DictType(
    DataType("String"),
    DataType("Double")
)); -- Dict<String,Double>
```

## TupleType

Builds the tuple type from the passed element types.

### Examples {#examples7}

```yql
SELECT FormatType(TupleType(
    DataType("String"),
    DataType("Double"),
    OptionalType(DataType("Bool"))
)); -- Tuple<String,Double,Bool?>
```

## StructType

Builds the structure type based on the passed element types. The standard syntax of named arguments is used to specify the element names.

### Examples {#examples8}

```yql
SELECT FormatType(StructType(
    DataType("Bool") AS MyBool,
    ListType(DataType("String")) AS StringList
)); -- Struct<'MyBool':Bool,'StringList':List<String>>
```

## VariantType

Returns the type of a variant based on the underlying type (structure or tuple).

### Examples {#examples9}

```yql
SELECT FormatType(VariantType(
  ParseType("Struct<foo:Int32,bar:Double>")
)); -- Variant<'bar':Double,'foo':Int32>
```

## ResourceType

Returns the type of the [resource](../types/special.md) based on the passed string label.

### Examples {#examples10}

```yql
SELECT FormatType(ResourceType("Foo")); -- Resource<'Foo'>
```

## CallableType

Constructs the type of the called value using the following arguments:

1. Number of optional arguments (if all arguments are required — 0).
2. Result type.
3. All the next arguments of CallableType are treated as types of arguments of the callable value, but with a shift for two required arguments (for example, the third argument of the CallableType describes the type of the first argument in the callable value).

### Examples {#examples11}

```yql
SELECT FormatType(CallableType(
  1, -- optional args count
  DataType("Double"), -- result type
  DataType("String"), -- arg #1 type
  OptionalType(DataType("Int64")) -- arg #2 type
)); -- Callable<(String,[Int64?])->Double>
```

## GenericType, UnitType, and VoidType {#generictype}

Return the same-name [special data types](../types/special.md). They have no arguments because they are not parameterized.

### Examples {#examples12}

```yql
SELECT FormatType(VoidType()); -- Void
```

## OptionalItemType, ListItemType and StreamItemType {#optionalitemtype}

If a type is passed to these functions, then they perform the action reverse to [OptionalType](types.md#optionaltype), [ListType](types.md#listtype), and [StreamType](types.md#listtype): return the item type based on its container type.

If a type handle is passed to these functions, then they perform the action reverse to [OptionalTypeHandle](types.md#optionaltypehandle), [ListTypeHandle](types.md#list-stream-typehandle), and [StreamTypeHandle](types.md#list-stream-typehandle): they return the handle of the element type based on the type handle of its container.

### Examples {#examples13}

```yql
SELECT FormatType(ListItemType(
  ParseType("List<Int32>")
)); -- Int32
```

```yql
SELECT FormatType(ListItemType(
  ParseTypeHandle("List<Int32>")
)); -- Int32
```

## DictKeyType and DictPayloadType {#dictkeytype}

Returns the type of the key or value based on the dictionary type.

### Examples {#examples14}

```yql
SELECT FormatType(DictKeyType(
  ParseType("Dict<Int32,String>")
)); -- Int32
```

## TupleElementType

Returns the tuple's element type based on the tuple type and the element index (index starts from zero).

### Examples {#examples15}

```yql
SELECT FormatType(TupleElementType(
  ParseType("Tuple<Int32,Double>"), "1"
)); -- Double
```

## StructMemberType

Returns the type of the structure element based on the structure type and element name.

### Examples {#examples16}

```yql
SELECT FormatType(StructMemberType(
  ParseType("Struct<foo:Int32,bar:Double>"), "foo"
)); -- Int32
```

## CallableResultType and CallableArgumentType {#callableresulttype}

`CallableResultType` returns the result type based on the type of the called value. `CallableArgumentType` returns the argument type based on the called value type and its index (index starts from zero).

### Examples {#examples17}

```yql
$callable_type = ParseType("(String,Bool)->Double");

SELECT FormatType(CallableResultType(
    $callable_type
)), -- Double
FormatType(CallableArgumentType(
    $callable_type, 1
)); -- Bool
```

## VariantUnderlyingType

If a type is passed to this function, then it an action reverse to [VariantType](types.md#varianttype): it returns the underlying type based on the variant type.

If a type handle is passed to this function, it performs the action reverse to [VariantTypeHandle](types.md#varianttypehandle): returns the handle of the underlying type based on the handle of the variant type.

### Examples {#examples18}

```yql
SELECT FormatType(VariantUnderlyingType(
  ParseType("Variant<foo:Int32,bar:Double>")
)), -- Struct<'bar':Double,'foo':Int32>
FormatType(VariantUnderlyingType(
  ParseType("Variant<Int32,Double>")
)); -- Tuple<Int32,Double>
```

```yql
SELECT FormatType(VariantUnderlyingType(
  ParseTypeHandle("Variant<foo:Int32,bar:Double>")
)), -- Struct<'bar':Double,'foo':Int32>
FormatType(VariantUnderlyingType(
  ParseTypeHandle("Variant<Int32,Double>")
)); -- Tuple<Int32,Double>
```

## Functions for data types during calculations

To work with data types during calculations, use handle types: these are [resources](../types/special.md) that contain an opaque type definition. After constructing the type handle, you can revert to the regular type using the [EvaluateType](types.md#evaluatetype) function. For debug purposes, you can convert a handle type to a string using the [FormatType](types.md#formattype) function.

### TypeHandle

Getting a type handle from the type passed to the argument.

#### Examples {#examples19}

```yql
SELECT FormatType(TypeHandle(TypeOf("foo")));  -- String
```

### EvaluateType

Getting the type from the type handle passed to the argument. The function is evaluated before the start of the main calculation, as well as [EvaluateExpr](basic.md#evaluate_expr_atom).

#### Examples {#examples20}

```yql
SELECT FormatType(EvaluateType(TypeHandle(TypeOf("foo"))));  -- String
```

### ParseTypeHandle

Building a type handle from a string with description. [Documentation for its format](../types/type_string.md).

#### Examples {#examples21}

```yql
SELECT FormatType(ParseTypeHandle("List<Int32>"));  -- List<int32>
```

### TypeKind

Getting the top-level type name from the type handle passed to the argument.

#### Examples {#examples22}

```yql
SELECT TypeKind(TypeHandle(TypeOf("foo")));  -- Data
SELECT TypeKind(ParseTypeHandle("List<Int32>"));  -- List
```

### DataTypeComponents

Getting the name and parameters for a [primitive data type](../types/primitive.md) from the primitive type handle passed to the argument. Reverse function: [DataTypeHandle](types.md#datatypehandle).

#### Examples {#examples23}

```yql
SELECT DataTypeComponents(TypeHandle(TypeOf("foo")));  -- ["String"]
SELECT DataTypeComponents(ParseTypeHandle("Decimal(4,1)"));  -- ["Decimal", "4", "1"]
```

### DataTypeHandle

Constructing a handle for a [primitive data type](../types/primitive.md) from its name and parameters passed to the argument as a list. Reverse function: [DataTypeComponents](types.md#datatypecomponents).

#### Examples {#examples24}

```yql
SELECT FormatType(DataTypeHandle(
    AsList("String")
)); -- String

SELECT FormatType(DataTypeHandle(
    AsList("Decimal", "4", "1")
)); -- Decimal(4,1)
```

### OptionalTypeHandle

Adds the option to assign `NULL` to the passed type handle.

#### Examples {#examples25}

```yql
SELECT FormatType(OptionalTypeHandle(
    TypeHandle(DataType("Bool"))
)); -- Bool?
```

### PgTypeName

Getting the name of the PostgreSQL type from the type handle passed to the argument. Inverse function: [PgTypeHandle](types.md#pgtypehandle).

#### Examples {#examples26}

```yql
SELECT PgTypeName(ParseTypeHandle("pgint4")); -- int4
```

### PgTypeHandle

Builds a type handle based on the passed name of the PostgreSQL type. Inverse function: [PgTypeName](types.md#pgtypename).

#### Examples {#examples27}

```yql
SELECT FormatType(PgTypeHandle("int4")); -- pgint4
```

### ListTypeHandle and StreamTypeHandle {#list-stream-typehandle}

Builds a list type handle or stream type handle based on the passed element type handle.

#### Examples {#examples28}

```yql
SELECT FormatType(ListTypeHandle(
    TypeHandle(DataType("Bool"))
)); -- List<Bool>
```

### EmptyListTypeHandle and EmptyDictTypeHandle

Constructs a handle for an empty list or dictionary.

#### Examples {#examples29}

```yql
SELECT FormatType(EmptyListTypeHandle()); -- EmptyList
```

### TupleTypeComponents

Getting a list of element type handles from the tuple type handle passed to the argument. Inverse function: [TupleTypeHandle](types.md#tupletypehandle).

#### Examples {#examples30}

```yql
SELECT ListMap(
   TupleTypeComponents(
       ParseTypeHandle("Tuple<Int32, String>")
   ),
   ($x)->{
       return FormatType($x)
   }
); -- ["Int32", "String"]
```

### TupleTypeHandle

Building a tuple type handle from handles of element types passed as a list to the argument. Inverse function: [TupleTypeComponents](types.md#tupletypecomponents).

#### Examples {#examples31}

```yql
SELECT FormatType(
    TupleTypeHandle(
        AsList(
            ParseTypeHandle("Int32"),
            ParseTypeHandle("String")
        )
    )
); -- Tuple<Int32,String>
```

### StructTypeComponents

Getting a list of element type handles and their names from the structure type handle passed to the argument. Inverse function: [StructTypeHandle](types.md#structtypehandle).

#### Examples {#examples32}

```yql
SELECT ListMap(
    StructTypeComponents(
        ParseTypeHandle("Struct<a:Int32, b:String>")
    ),
    ($x) -> {
        return AsTuple(
            FormatType($x.Type),
            $x.Name
        )
    }
); -- [("Int32","a"), ("String","b")]
```

### StructTypeHandle

Building a structure type handle from handles of element types and names passed as a list to the argument. Inverse function: [StructTypeComponents](types.md#structtypecomponents).

#### Examples {#examples33}

```yql
SELECT FormatType(
    StructTypeHandle(
        AsList(
            AsStruct(ParseTypeHandle("Int32") as Type,"a" as Name),
            AsStruct(ParseTypeHandle("String") as Type, "b" as Name)
        )
    )
); -- Struct<'a':Int32,'b':String>
```

### DictTypeComponents

Getting a key-type handle and a value-type handle from the dictionary-type handle passed to the argument. Inverse function: [DictTypeHandle](types.md#dicttypehandle).

#### Examples {#examples34}

```yql
$d = DictTypeComponents(ParseTypeHandle("Dict<Int32,String>"));

SELECT
    FormatType($d.Key),     -- Int32
    FormatType($d.Payload); -- String
```

### DictTypeHandle

Building a dictionary-type handle from a key-type handle and a value-type handle passed to arguments. Inverse function: [DictTypeComponents](types.md#dicttypecomponents).

#### Examples {#examples35}

```yql
SELECT FormatType(
    DictTypeHandle(
        ParseTypeHandle("Int32"),
        ParseTypeHandle("String")
    )
); -- Dict<Int32, String>
```

### ResourceTypeTag

Getting the tag from the resource type handle passed to the argument. Inverse function: [ResourceTypeHandle](types.md#resourcetypehandle).

#### Examples {#examples36}

```yql
SELECT ResourceTypeTag(ParseTypeHandle("Resource<foo>")); -- foo
```

### ResourceTypeHandle

Building a resource-type handle from the tag value passed to the argument. Inverse function: [ResourceTypeTag](types.md#resourcetypetag).

#### Examples {#examples37}

```yql
SELECT FormatType(ResourceTypeHandle("foo")); -- Resource<'foo'>
```

### TaggedTypeComponents

Getting the tag and the basic type from the decorated type handle passed to the argument. Inverse function: [TaggedTypeHandle](types.md#taggedtypehandle).

#### Examples {#examples38}

```yql
$t = TaggedTypeComponents(ParseTypeHandle("Tagged<Int32,foo>"));

SELECT FormatType($t.Base), $t.Tag; -- Int32, foo
```

### TaggedTypeHandle

Constructing a decorated type handle based on the base type handle and the tag name passed in arguments. Inverse function: [TaggedTypeComponents](types.md#taggedtypecomponents).

#### Examples {#examples39}

```yql
SELECT FormatType(TaggedTypeHandle(
    ParseTypeHandle("Int32"), "foo"
)); -- Tagged<Int32, 'foo'>
```

### VariantTypeHandle

Building a variant-type handle from the handle of the underlying type passed to the argument. Inverse function: [VariantUnderlyingType](types.md#variantunderlyingtype).

#### Examples {#examples40}

```yql
SELECT FormatType(VariantTypeHandle(
    ParseTypeHandle("Tuple<Int32, String>")
)); -- Variant<Int32, String>
```

### VoidTypeHandle and NullTypeHandle

Constructing a handle for Void and Null types, respectively.

#### Examples {#examples41}

```yql
SELECT FormatType(VoidTypeHandle()); -- Void
SELECT FormatType(NullTypeHandle()); -- Null
```

### CallableTypeComponents

Getting the handle description for the type of callable value passed to the argument. Inverse function: [CallableTypeHandle](types.md#callabletypehandle).

#### Examples {#examples42}

```yql
$formatArgument = ($x) -> {
    return AsStruct(
        FormatType($x.Type) as Type,
        $x.Name as Name,
        $x.Flags as Flags
    )
};

$formatCallable = ($x) -> {
    return AsStruct(
        $x.OptionalArgumentsCount as OptionalArgumentsCount,
        $x.Payload as Payload,
        FormatType($x.Result) as Result,
        ListMap($x.Arguments, $formatArgument) as Arguments
    )
};

SELECT $formatCallable(
    CallableTypeComponents(
        ParseTypeHandle("(Int32,[bar:Double?{Flags:AutoMap}])->String")
    )
);  -- (OptionalArgumentsCount: 1, Payload: "", Result: "String", Arguments: [
    --   (Type: "Int32", Name: "", Flags: []),
    --   (Type: "Double?", Name: "bar", Flags: ["AutoMap"]),
    -- ])
```

### CallableArgument

Packing the description of the argument of the callable value into the structure to be passed to the [CallableTypeHandle](types.md#callabletypehandle) function with the following arguments:

1. Argument type handle.
2. Optional argument name. The default value is an empty string.
3. A list of strings with optional argument flags. The default value is an empty list. Supported flags are "AutoMap".

### CallableTypeHandle

Constructing the type handle of the called value using the following arguments:

1. Handle of the return value type.
2. List of descriptions of arguments received using the [CallableArgument](types.md#callableargument) function.
3. Optional number of optional arguments in the callable value. The default value is 0.
4. An optional label for the called value type. The default value is an empty string.

Inverse function: [CallableTypeComponents](types.md#callabletypecomponents).

#### Examples {#examples43}

```yql
SELECT FormatType(
    CallableTypeHandle(
        ParseTypeHandle("String"),
        AsList(
            CallableArgument(ParseTypeHandle("Int32")),
            CallableArgument(ParseTypeHandle("Double?"), "bar", AsList("AutoMap"))
        ),
        1
    )
);  -- Callable<(Int32,['bar':Double?{Flags:AutoMap}])->String>
```

### LambdaArgumentsCount

Getting the number of arguments in a lambda function.

#### Examples {#examples44}

```yql
SELECT LambdaArgumentsCount(($x, $y)->($x+$y))
; -- 2
```
