# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AcoustAppData.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='AcoustAppData.proto',
  package='',
  serialized_pb=_b('\n\x13\x41\x63oustAppData.proto\".\n\rAcoustAppData\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x02(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ACOUSTAPPDATA = _descriptor.Descriptor(
  name='AcoustAppData',
  full_name='AcoustAppData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='AcoustAppData.address', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='AcoustAppData.data', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=69,
)

DESCRIPTOR.message_types_by_name['AcoustAppData'] = _ACOUSTAPPDATA

AcoustAppData = _reflection.GeneratedProtocolMessageType('AcoustAppData', (_message.Message,), dict(
  DESCRIPTOR = _ACOUSTAPPDATA,
  __module__ = 'AcoustAppData_pb2'
  # @@protoc_insertion_point(class_scope:AcoustAppData)
  ))
_sym_db.RegisterMessage(AcoustAppData)


# @@protoc_insertion_point(module_scope)
