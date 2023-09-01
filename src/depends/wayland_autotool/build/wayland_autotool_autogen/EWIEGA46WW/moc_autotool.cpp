/****************************************************************************
** Meta object code from reading C++ file 'autotool.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.11.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../autotool.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'autotool.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.11.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_AutoTool_t {
    QByteArrayData data[24];
    char stringdata0[175];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_AutoTool_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_AutoTool_t qt_meta_stringdata_AutoTool = {
    {
QT_MOC_LITERAL(0, 0, 8), // "AutoTool"
QT_MOC_LITERAL(1, 9, 15), // "D-Bus Interface"
QT_MOC_LITERAL(2, 25, 19), // "com.deepin.Autotool"
QT_MOC_LITERAL(3, 45, 5), // "click"
QT_MOC_LITERAL(4, 51, 0), // ""
QT_MOC_LITERAL(5, 52, 6), // "method"
QT_MOC_LITERAL(6, 59, 9), // "mouseDown"
QT_MOC_LITERAL(7, 69, 7), // "mouseUp"
QT_MOC_LITERAL(8, 77, 6), // "moveTo"
QT_MOC_LITERAL(9, 84, 1), // "x"
QT_MOC_LITERAL(10, 86, 1), // "y"
QT_MOC_LITERAL(11, 88, 6), // "getPos"
QT_MOC_LITERAL(12, 95, 7), // "getSize"
QT_MOC_LITERAL(13, 103, 7), // "keyDown"
QT_MOC_LITERAL(14, 111, 3), // "key"
QT_MOC_LITERAL(15, 115, 5), // "keyUp"
QT_MOC_LITERAL(16, 121, 5), // "press"
QT_MOC_LITERAL(17, 127, 7), // "vscroll"
QT_MOC_LITERAL(18, 135, 5), // "delta"
QT_MOC_LITERAL(19, 141, 7), // "hscroll"
QT_MOC_LITERAL(20, 149, 7), // "setText"
QT_MOC_LITERAL(21, 157, 4), // "text"
QT_MOC_LITERAL(22, 162, 7), // "getText"
QT_MOC_LITERAL(23, 170, 4) // "init"

    },
    "AutoTool\0D-Bus Interface\0com.deepin.Autotool\0"
    "click\0\0method\0mouseDown\0mouseUp\0moveTo\0"
    "x\0y\0getPos\0getSize\0keyDown\0key\0keyUp\0"
    "press\0vscroll\0delta\0hscroll\0setText\0"
    "text\0getText\0init"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_AutoTool[] = {

 // content:
       7,       // revision
       0,       // classname
       1,   14, // classinfo
      14,   16, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // classinfo: key, value
       1,    2,

 // slots: name, argc, parameters, tag, flags
       3,    1,   86,    4, 0x0a /* Public */,
       6,    1,   89,    4, 0x0a /* Public */,
       7,    1,   92,    4, 0x0a /* Public */,
       8,    2,   95,    4, 0x0a /* Public */,
      11,    0,  100,    4, 0x0a /* Public */,
      12,    0,  101,    4, 0x0a /* Public */,
      13,    1,  102,    4, 0x0a /* Public */,
      15,    1,  105,    4, 0x0a /* Public */,
      16,    1,  108,    4, 0x0a /* Public */,
      17,    1,  111,    4, 0x0a /* Public */,
      19,    1,  114,    4, 0x0a /* Public */,
      20,    1,  117,    4, 0x0a /* Public */,
      22,    0,  120,    4, 0x0a /* Public */,
      23,    0,  121,    4, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void, QMetaType::QString,    5,
    QMetaType::Void, QMetaType::QString,    5,
    QMetaType::Void, QMetaType::QString,    5,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,    9,   10,
    QMetaType::QPointF,
    QMetaType::QPoint,
    QMetaType::Void, QMetaType::UInt,   14,
    QMetaType::Void, QMetaType::UInt,   14,
    QMetaType::Void, QMetaType::UInt,   14,
    QMetaType::Void, QMetaType::QReal,   18,
    QMetaType::Void, QMetaType::QReal,   18,
    QMetaType::Void, QMetaType::QString,   21,
    QMetaType::QString,
    QMetaType::Void,

       0        // eod
};

void AutoTool::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        AutoTool *_t = static_cast<AutoTool *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->click((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->mouseDown((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 2: _t->mouseUp((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 3: _t->moveTo((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 4: { QPointF _r = _t->getPos();
            if (_a[0]) *reinterpret_cast< QPointF*>(_a[0]) = std::move(_r); }  break;
        case 5: { QPoint _r = _t->getSize();
            if (_a[0]) *reinterpret_cast< QPoint*>(_a[0]) = std::move(_r); }  break;
        case 6: _t->keyDown((*reinterpret_cast< quint32(*)>(_a[1]))); break;
        case 7: _t->keyUp((*reinterpret_cast< quint32(*)>(_a[1]))); break;
        case 8: _t->press((*reinterpret_cast< quint32(*)>(_a[1]))); break;
        case 9: _t->vscroll((*reinterpret_cast< qreal(*)>(_a[1]))); break;
        case 10: _t->hscroll((*reinterpret_cast< qreal(*)>(_a[1]))); break;
        case 11: _t->setText((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 12: { QString _r = _t->getText();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 13: _t->init(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject AutoTool::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_AutoTool.data,
      qt_meta_data_AutoTool,  qt_static_metacall, nullptr, nullptr}
};


const QMetaObject *AutoTool::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *AutoTool::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_AutoTool.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int AutoTool::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 14)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 14;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 14)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 14;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
