## Lorem Ipsum

1. Git clone the catalog connector PR.
1. From this repository copy `src/mlx-catalog.json` to the `elyra/elyra/metadata/schemas` directory.
1. From this repository copy `src/mlx_component_catalog_connector.py` to the `elyra/elyra/pipeline` directory.
1. In `setup.py` add the last line shown below
   ```
           'elyra.component.catalog_types': [
            'url-catalog = elyra.pipeline.component_reader:UrlComponentCatalogConnector',
            'local-file-catalog = elyra.pipeline.component_reader:FilesystemComponentCatalogConnector',
            'local-directory-catalog = elyra.pipeline.component_reader:DirectoryComponentCatalogConnector',
            'mlx-catalog = elyra.pipeline.mlx_component_catalog_connector:MLXComponentCatalogConnector'
   ```
1. Rebuild Elyra.   