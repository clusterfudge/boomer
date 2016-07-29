import os
import pdoc
__author__ = 'seanfitz'

DOCS_NAME = "boomer-skills-sdk"

DOC_OUTPUT_DIR = "build/doc/%s/html" % DOCS_NAME

documented_sdk_modules = [
        "boomer.configuration",
        "boomer.configuration.config",
        "boomer.dialog",
        "boomer.filesystem",
        "boomer.session",
        "boomer.util",
        "boomer.util.log"
    ]


def module_to_docpath(module_name):
    module_source_dir = module_name.replace(".", "/")
    module_doc_dir = os.path.join(DOC_OUTPUT_DIR, module_source_dir)
    base_module_name = os.path.basename(module_doc_dir)
    if not os.path.isdir(module_source_dir):
        d = os.path.dirname(module_doc_dir)
        try:
            os.makedirs(d)
        except OSError:
            pass
        return os.path.join(d, base_module_name + '.m.html')
    else:
        try:
            os.makedirs(module_doc_dir)
        except OSError:
            pass
        return os.path.join(module_doc_dir, 'index.html')


def main():
    for m in documented_sdk_modules:
        html = pdoc.html(m, allsubmodules=True)
        with open(module_to_docpath(m), 'w') as f:
            f.write(html)
    import boomer
    boomer.__all__ = [m[8:] for m in documented_sdk_modules]
    root_module = pdoc.Module(boomer)
    html = root_module.html(external_links=False, link_prefix='', source=True)
    with open(module_to_docpath("boomer"), 'w') as f:
            f.write(html)


if __name__ == "__main__":
    main()
