======================
Document get transform
======================

Simple HTTP transform to GET a resource, encode it as a BASE64 encoded string and return it with the original entity as an injected JSON string

Configuration
-------------

You can configure the service with the following environment variables:

.. list-table::
   :header-rows: 1
   :widths: 10, 50, 30, 10

   * - Variable
     - Description
     - Default
     - Req

   * - ``URL_PROPERTY``
     - The field to use to find the URL to GET
     - ``"gdpr-document:content-exctract"``
     -

   * - ``RETURN_PROPERTY``
     - What property name to use for the returned BASE64 encoded data
     - ``"gdpr-document:content"``
     -
