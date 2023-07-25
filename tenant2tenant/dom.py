# ./tenant2tenant/dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:dd0c54b27145938df61cb596ddb301f100abc046
# Generated 2022-03-01 11:44:55.719755 by PyXB version 1.2.7-DEV using Python 3.10.2.final.0
# Namespace http://xml.homeinfo.de/schema/tenant2tenant

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier(
    "urn:uuid:a2093b4a-994c-11ec-a1c5-7427eaa9df7d"
)

# Version of PyXB used to generate the bindings
_PyXBVersion = "1.2.7-DEV"
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI(
    "http://xml.homeinfo.de/schema/tenant2tenant", create_if_missing=True
)
Namespace.configureCategories(["typeBinding", "elementBinding"])


def CreateFromDocument(
    xml_text, fallback_namespace=None, location_base=None, default_namespace=None
):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword fallback_namespace An absent L{pyxb.Namespace} instance
    to use for unqualified names when there is no default namespace in
    scope.  If unspecified or C{None}, the namespace of the module
    containing this function will be used, if it is an absent
    namespace.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.

    @keyword default_namespace An alias for @c fallback_namespace used
    in PyXB 1.1.4 through 1.2.6.  It behaved like a default namespace
    only for absent namespaces.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(
        fallback_namespace=fallback_namespace, location_base=location_base
    )
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance


def CreateFromDOM(node, fallback_namespace=None, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}.
    """
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, fallback_namespace)


# Complex type {http://xml.homeinfo.de/schema/tenant2tenant}TenantToTenant with content type ELEMENT_ONLY
class TenantToTenant(pyxb.binding.basis.complexTypeDefinition):
    """
    Mieter-zu-Mieter Nachrichten.
    """

    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, "TenantToTenant")
    _XSDLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 22, 4
    )
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element message uses Python identifier message
    __message = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(None, "message"),
        "message",
        "__httpxml_homeinfo_deschematenant2tenant_TenantToTenant_message",
        True,
        pyxb.utils.utility.Location(
            "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 29, 12
        ),
    )

    message = property(
        __message.value,
        __message.set,
        None,
        "\n                      Mieter-zu-Mieter Nachrichten.\n                    ",
    )

    _ElementMap.update({__message.name(): __message})
    _AttributeMap.update({})


_module_typeBindings.TenantToTenant = TenantToTenant
Namespace.addCategoryObject("typeBinding", "TenantToTenant", TenantToTenant)


# Complex type {http://xml.homeinfo.de/schema/tenant2tenant}TenantMessage with content type SIMPLE
class TenantMessage(pyxb.binding.basis.complexTypeDefinition):
    """
    Mieter-zu-Mieter Nachricht.
    """

    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, "TenantMessage")
    _XSDLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 40, 4
    )
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string

    # Attribute created uses Python identifier created
    __created = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(None, "created"),
        "created",
        "__httpxml_homeinfo_deschematenant2tenant_TenantMessage_created",
        pyxb.binding.datatypes.dateTime,
        required=True,
    )
    __created._DeclarationLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 48, 10
    )
    __created._UseLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 48, 10
    )

    created = property(
        __created.value,
        __created.set,
        None,
        "\n                      Zeitstempel der Erstellung.\n                  ",
    )

    # Attribute released uses Python identifier released
    __released = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(None, "released"),
        "released",
        "__httpxml_homeinfo_deschematenant2tenant_TenantMessage_released",
        pyxb.binding.datatypes.boolean,
    )
    __released._DeclarationLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 55, 10
    )
    __released._UseLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 55, 10
    )

    released = property(
        __released.value,
        __released.set,
        None,
        "\n                      Freigabe-Flag.\n                  ",
    )

    # Attribute startDate uses Python identifier startDate
    __startDate = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(None, "startDate"),
        "startDate",
        "__httpxml_homeinfo_deschematenant2tenant_TenantMessage_startDate",
        pyxb.binding.datatypes.date,
    )
    __startDate._DeclarationLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 62, 10
    )
    __startDate._UseLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 62, 10
    )

    startDate = property(
        __startDate.value,
        __startDate.set,
        None,
        "\n                      Datum des Anzeigebeginns.\n                  ",
    )

    # Attribute endDate uses Python identifier endDate
    __endDate = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(None, "endDate"),
        "endDate",
        "__httpxml_homeinfo_deschematenant2tenant_TenantMessage_endDate",
        pyxb.binding.datatypes.date,
    )
    __endDate._DeclarationLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 69, 10
    )
    __endDate._UseLocation = pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 69, 10
    )

    endDate = property(
        __endDate.value,
        __endDate.set,
        None,
        "\n                      Datum des Anzeigeendes.\n                  ",
    )

    _ElementMap.update({})
    _AttributeMap.update(
        {
            __created.name(): __created,
            __released.name(): __released,
            __startDate.name(): __startDate,
            __endDate.name(): __endDate,
        }
    )


_module_typeBindings.TenantMessage = TenantMessage
Namespace.addCategoryObject("typeBinding", "TenantMessage", TenantMessage)


tenant2tenant = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(Namespace, "tenant2tenant"),
    TenantToTenant,
    documentation="\n                Mieter-zu-Mieter Nachrichten.\n            ",
    location=pyxb.utils.utility.Location(
        "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 13, 4
    ),
)
Namespace.addCategoryObject(
    "elementBinding", tenant2tenant.name().localName(), tenant2tenant
)


TenantToTenant._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(None, "message"),
        TenantMessage,
        scope=TenantToTenant,
        documentation="\n                      Mieter-zu-Mieter Nachrichten.\n                    ",
        location=pyxb.utils.utility.Location(
            "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 29, 12
        ),
    )
)


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 29, 12
        ),
    )
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        TenantToTenant._UseForTag(pyxb.namespace.ExpandedName(None, "message")),
        pyxb.utils.utility.Location(
            "/home/neumann/Projekte/tenant2tenant/files/tenant2tenant.xsd", 29, 12
        ),
    )
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False,
    )
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [fac.UpdateInstruction(cc_0, True)]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)


TenantToTenant._Automaton = _BuildAutomaton()
