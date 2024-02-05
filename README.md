# Using R and Python in a collaborative research project

This is an intermediate level workshop that will teach best practices of using Python and R together within a single research project. I walk participants through steps of a mini project involving data analysis and visualization, highlighting use of free and open source tools and challenges of collaboration on research code. This workshop uses economic, demographic and geographic data characterizing US communities that is freely and publicly available from the US Census Bureau and the USDA Economic Research Service websites. Prior experience with R or Python is recommended.

Workshop topics:
- introduction and challenges of multi-language collaborative projects
- setting up a portable computational environment with `conda` and `renv`
- data retrieval and preparation in Python
- using Python from R with `reticulate`
- basic regression analysis in R
- using R from Python with `rpy2`
- interactive presentation of results with Python in a Jupyter notebook

This workshop will be conducted by Anton Babkin at the 2024 Data Science Research Bazaar, University of Wisconsin-Madison, February 7, 2024.

## Setup

To follow along with the workshop, you need to have the stack of tools installed on your computer.

1. Install [R](https://cran.rstudio.com/) and [RStudio](https://posit.co/download/rstudio-desktop/).

2. Install `conda` + `mamba`. [Instructions](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html).

3. Clone this repository to your computer. Open RStudio and select File -> New Project... -> Version Control -> Git, enter this repository URL: `https://github.com/antonbabkin/workshop-pythonr`  
You can also clone using your preferred Git tool and then open project in RStudio.

4. Install [renv](https://rstudio.github.io/renv/) and required R packages. Packages will be installed according to specification listed in the `DESCRIPTION` file. Make sure you have the `workshop-pythonr` project open in RStudio and run the following commands in Console:
    ```
    install.packages("renv")
    renv::init(bare = TRUE)
    renv::install()
    ```

5. Install required Python packages into a new [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). Using `mamba` for this will typically work better. In a terminal, navigate to the repository folder and create the environment specified in the `environment.yml` file.
    ```
    cd workshop-pythonr
    mamba env create -f environment.yml
    ```

6. Activate conda environment and start Jupyter Lab to work with Python notebooks.
    ```
    conda activate workshop-pythonr
    jupyter lab
    ```


## License

Project code is licensed under the [MIT license](LICENSE.md). All other content is licensed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/).
