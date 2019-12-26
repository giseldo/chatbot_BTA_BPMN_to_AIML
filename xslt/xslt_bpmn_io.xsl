<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
                targetNamespace="http://bpmn.io/schema/bpmn">

    <xsl:template match="/">
        <bpmn>

            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:sequenceFlow">
                <edge>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="ant">
                        <xsl:value-of select='@sourceRef'/>
                    </xsl:attribute>
                    <xsl:attribute name="pos">
                        <xsl:value-of select='@targetRef'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </edge>
            </xsl:for-each>

            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:task">
                <task>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </task>
            </xsl:for-each>

            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:startEvent">
                <start_event>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </start_event>
            </xsl:for-each>

            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:exclusiveGateway">
                <exclusive_gateway>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </exclusive_gateway>
            </xsl:for-each>

             <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:endEvent">
                <end_event>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </end_event>
            </xsl:for-each>


            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:textAnnotation">
                <text_association>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='bpmn:text'/>
                    </xsl:attribute>
                </text_association>
            </xsl:for-each>

            <xsl:for-each select="bpmn:definitions/bpmn:process/bpmn:association">
                <association>
                    <xsl:attribute name="id">
                        <xsl:value-of select='@id'/>
                    </xsl:attribute>
                    <xsl:attribute name="ant">
                        <xsl:value-of select='@sourceRef'/>
                    </xsl:attribute>
                    <xsl:attribute name="pos">
                        <xsl:value-of select='@targetRef'/>
                    </xsl:attribute>
                    <xsl:attribute name="nome">
                        <xsl:value-of select='@name'/>
                    </xsl:attribute>
                </association>
            </xsl:for-each>

        </bpmn>
    </xsl:template>

</xsl:stylesheet>