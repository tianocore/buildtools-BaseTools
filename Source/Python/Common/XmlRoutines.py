## @file
# This is an XML API that uses a syntax similar to XPath, but it is written in
# standard python so that no extra python packages are required to use it.
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import xml.dom.minidom

## Get a list of XML nodes using XPath style syntax.
#
# Return a list of XML DOM nodes from the root Dom specified by XPath String.
# If the input Dom or String is not valid, then an empty list is returned.
#
# @param  Dom                The root XML DOM node.
# @param  String             A XPath style path.
#
# @revel  Nodes              A list of XML nodes matching XPath style Sting.
#
def XmlList(Dom, String):
    if String == None or String == "" or Dom == None or Dom == "":
        return []
    if Dom.nodeType == Dom.DOCUMENT_NODE:
        Dom = Dom.documentElement
    if String[0] == "/":
        String = String[1:]
    TagList = String.split('/')
    Nodes = [Dom]
    Index = 0
    End = len(TagList) - 1
    while Index <= End:
        ChildNodes = []
        for Node in Nodes:
            if Node.nodeType == Node.ELEMENT_NODE and Node.tagName == TagList[Index]:
                if Index < End:
                    ChildNodes.extend(Node.childNodes)
                else:
                    ChildNodes.append(Node)
        Nodes = ChildNodes
        ChildNodes = []
        Index += 1

    return Nodes


## Get a single XML node using XPath style syntax.
#
# Return a single XML DOM node from the root Dom specified by XPath String.
# If the input Dom or String is not valid, then an empty string is returned.
#
# @param  Dom                The root XML DOM node.
# @param  String             A XPath style path.
#
# @revel  Node               A single XML node matching XPath style Sting.
#
def XmlNode(Dom, String):
    if String == None or String == ""  or Dom == None or Dom == "":
        return ""
    if Dom.nodeType == Dom.DOCUMENT_NODE:
        Dom = Dom.documentElement
    if String[0] == "/":
        String = String[1:]
    TagList = String.split('/')
    Index = 0
    End = len(TagList) - 1
    ChildNodes = [Dom]
    while Index <= End:
        for Node in ChildNodes:
            if Node.nodeType == Node.ELEMENT_NODE and Node.tagName == TagList[Index]:
                if Index < End:
                    ChildNodes = Node.childNodes
                else:
                    return Node
                break
        Index += 1
    return ""


## Get a single XML element using XPath style syntax.
#
# Return a single XML element from the root Dom specified by XPath String.
# If the input Dom or String is not valid, then an empty string is returned.
#
# @param  Dom                The root XML DOM object.
# @param  Strin              A XPath style path.
#
# @revel  Element            An XML element matching XPath style Sting.
#
def XmlElement(Dom, String):
    try:
        return XmlNode(Dom, String).firstChild.data.strip()
    except:
        return ""


## Get a single XML element of the current node.
#
# Return a single XML element specified by the current root Dom.
# If the input Dom is not valid, then an empty string is returned.
#
# @param  Dom                The root XML DOM object.
#
# @revel  Element            An XML element in current root Dom.
#
def XmlElementData(Dom):
    try:
        return Dom.firstChild.data.strip()
    except:
        return ""


## Get a list of XML elements using XPath style syntax.
#
# Return a list of XML elements from the root Dom specified by XPath String.
# If the input Dom or String is not valid, then an empty list is returned.
#
# @param  Dom                The root XML DOM object.
# @param  String             A XPath style path.
#
# @revel  Elements           A list of XML elements matching XPath style Sting.
#
def XmlElementList(Dom, String):
    return map(XmlElementData, XmlList(Dom, String))


## Get the XML attribute of the current node.
#
# Return a single XML attribute named Attribute from the current root Dom.
# If the input Dom or Attribute is not valid, then an empty string is returned.
#
# @param  Dom                The root XML DOM object.
# @param  Attribute          The name of Attribute.
#
# @revel  Element            A single XML element matching XPath style Sting.
#
def XmlAttribute(Dom, Attribute):
    try:
        return Dom.getAttribute(Attribute).strip()
    except:
        return ''


## Get the XML node name of the current node.
#
# Return a single XML node name from the current root Dom.
# If the input Dom is not valid, then an empty string is returned.
#
# @param  Dom                The root XML DOM object.
#
# @revel  Element            A single XML element matching XPath style Sting.
#
def XmlNodeName(Dom):
    try:
        return Dom.nodeName.strip()
    except:
        return ''

## Parse an XML file.
#
# Parse the input XML file named FileName and return a XML DOM it stands for.
# If the input File is not a valid XML file, then an empty string is returned.
#
# @param  FileName           The XML file name.
#
# @revel  Dom                The Dom object achieved from the XML file.
#
def XmlParseFile(FileName):
    try:
        XmlFile = open(FileName)
        Dom = xml.dom.minidom.parse(XmlFile)
        XmlFile.close()
        return Dom
    except:
        return ""


# This acts like the main() function for the script, unless it is 'import'ed
# into another script.
if __name__ == '__main__':
    # Nothing to do here. Could do some unit tests.
    pass
