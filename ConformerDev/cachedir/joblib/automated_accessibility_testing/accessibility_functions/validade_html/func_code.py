# first line: 93
def validade_html(html_recebido: str):
    vld = HTMLValidator()
    vld.validate_fragment(str(html_recebido))
    exceptions_list = []

    for error in vld.errors:
        exceptions_list.append(
            exceptions.AcessibilityException(
                "StaticHTMLValidation",
                error["extract"].replace("\n", ""),
                error["message"],
                error["hiliteStart"],
                error["hiliteLength"],
            )
        )
    return exceptions_list
