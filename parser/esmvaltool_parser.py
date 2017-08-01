import ConfigParser
import os
import sys

class Namelist:
    """
    Class to hold the Namelist parser information
    """
    def __init__(self):
        self.__name__ = "Namelist"
        self.__author__ = "Valeriu Predoi, University of Reading, valeriu.predoi@mcas.ac.uk"

    def s2b(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError

    def get_par_file(self, params_file):
        """
        Gets the params file or exists if not found
        """
        # ---- Check the params_file exists
        if not os.path.isfile(params_file):
            print >> sys.stderr,"Error: non existent parameter file: ", \
                params_file
            sys.exit(1)
        cp = ConfigParser.ConfigParser()
        cp.read(params_file)
        return cp

    # parse GLOBAL
    def GLOBAL(self, params_file):
        """
        Function to build dictionary containing
        the GLOBAL attributes. Takes ConfigParser object cp
        """
        cp = self.get_par_file(params_file)
        GLOB = {}
        if cp.has_option('GLOBAL','ini-version') :
            ini_version = int(cp.get('GLOBAL','ini-version'))
            GLOB['ini-version'] = ini_version
        if cp.has_option('GLOBAL','write_plots') :
            write_plots = self.s2b(cp.get('GLOBAL','write_plots'))
            GLOB['write_plots'] = write_plots
        if cp.has_option('GLOBAL','write_netcdf') :
            write_netcdf = self.s2b(cp.get('GLOBAL','write_netcdf'))
            GLOB['write_netcdf'] = write_netcdf
        if cp.has_option('GLOBAL','verbosity') :
            verbosity = int(cp.get('GLOBAL','verbosity'))
            GLOB['verbosity'] = verbosity
        if cp.has_option('GLOBAL','exit_on_warning') :
            eow = self.s2b(cp.get('GLOBAL','exit_on_warning'))
            GLOB['exit_on_warning'] = eow
        if cp.has_option('GLOBAL','output_file_type') :
            output_type = cp.get('GLOBAL','output_file_type')
            GLOB['output_file_type'] = output_type
        if cp.has_option('GLOBAL','climo_dir') :
            climo_dir = cp.get('GLOBAL','climo_dir')
            GLOB['climo_dir'] = climo_dir
        if cp.has_option('GLOBAL','wrk_dir') :
            work_dir = cp.get('GLOBAL','wrk_dir')
            GLOB['wrk_dir'] = work_dir
        if cp.has_option('GLOBAL','plot_dir') :
            plot_dir = cp.get('GLOBAL','plot_dir')
            GLOB['plot_dir'] = plot_dir
        return GLOB

    # parse PREPROCESS
    def PREPROCESS(self, params_file):
        """
        Function to build list of dictionaries containing
        the PREPROCESS attributes. Takes ConfigParser object cp
        """
        cp = self.get_par_file(params_file)
        if cp.has_option('PREPROCESS','id') :
            ids = cp.get('PREPROCESS','id').split('~')
        if cp.has_option('PREPROCESS','select_level') :
            select_level = [int(a) for a in cp.get('PREPROCESS','select_level').split('~')]
        if cp.has_option('PREPROCESS','target_grid') :
            target_grid = cp.get('PREPROCESS','target_grid').split('~')
        if cp.has_option('PREPROCESS','regrid_scheme') :
            regrid_scheme = cp.get('PREPROCESS','regrid_scheme').split('~')
        if cp.has_option('PREPROCESS','mask_fillvalues') :
            mask_fillvalues = [self.s2b(a) for a in cp.get('PREPROCESS','mask_fillvalues').split('~')]
        if cp.has_option('PREPROCESS','mask_landocean') :
            mask_landocean = cp.get('PREPROCESS','mask_landocean').split('~')
        if cp.has_option('PREPROCESS','multimodel_mean') :
            multimodel_mean = [self.s2b(a) for a in cp.get('PREPROCESS','multimodel_mean').split('~')]

        # construct a list of dictionaries for each preprocessor
        preprocs = []
        for i in range(len(ids)):
            PP = {}
            PP['id'] = ids[i]
            PP['select_level'] = select_level[i]
            PP['target_grid'] = target_grid[i]
            PP['regrid_scheme'] = regrid_scheme[i]
            PP['mask_fillvalues'] = mask_fillvalues[i]
            PP['mask_landocean'] = mask_landocean[i]
            PP['multimodel_mean'] = multimodel_mean[i]
            preprocs.append(PP)
        return preprocs

    # parse MODELS
    def MODELS(self, params_file):
        """
        Function to build list of dictionaries containing
        the MODELS attributes. Takes ConfigParser object cp
        """
        cp = self.get_par_file(params_file)
        if cp.has_option('MODELS','names') :
            model_names = cp.get('MODELS','names').split(',')
        if cp.has_option('MODELS','projects') :
            model_projects = cp.get('MODELS','projects').split(',')
        if cp.has_option('MODELS','mips') :
            model_mips = cp.get('MODELS','mips').split(',')
        if cp.has_option('MODELS','experiments') :
            model_exps = cp.get('MODELS','experiments').split(',')
        if cp.has_option('MODELS','ensembles') :
            model_ens = cp.get('MODELS','ensembles').split(',')
        if cp.has_option('MODELS','starts') :
            model_starts = [int(a) for a in cp.get('MODELS','starts').split(',')]
        if cp.has_option('MODELS','ends') :
            model_ends = [int(a) for a in cp.get('MODELS','ends').split(',')]
        if cp.has_option('MODELS','paths') :
            model_paths = cp.get('MODELS','paths').split(',')

        # construct a list of dictionaries for each model
        models = []
        for i in range(len(model_names)):
            MOD = {}
            MOD['name'] = model_names[i]
            MOD['project'] = model_projects[i]
            MOD['mip'] = model_mips[i]
            MOD['experiment'] = model_exps[i]
            MOD['ensemble'] = model_ens[i]
            MOD['start_year'] = str(model_starts[i])
            MOD['end_year'] = str(model_ends[i])
            MOD['dir'] = model_paths[i]
            models.append(MOD)
        if len(models) == 0:
            print >> sys.stderr, "No models specified in the Namelist file, exiting", params_file
            sys.exit(1)
        else:
            #for j in range(len(models)):
            #    print(models[j])
            return models

    # parse diagnostics
    # supports multiple diagnostics/variables delimited by "~"
    def DIAGNOSTICS(self, params_file):
        """
        Function to build list of dictionaries containing
        the DIAGNOSTIC attributes. Takes ConfigParser object cp
        """
        cp = self.get_par_file(params_file)
        if cp.has_option('DIAGNOSTIC','id') :
            diag_ids = cp.get('DIAGNOSTIC','id').split('~')
        if cp.has_option('DIAGNOSTIC','tags') :
            diag_tags = cp.get('DIAGNOSTIC','tags').split('~')
        if cp.has_option('DIAGNOSTIC','variable_names') :
            diag_vars = cp.get('DIAGNOSTIC','variable_names').split('~')
        if cp.has_option('DIAGNOSTIC','id') :
            diag_refs = cp.get('DIAGNOSTIC','ref_model').split('~')
        if cp.has_option('DIAGNOSTIC','field') :
            diag_fields = cp.get('DIAGNOSTIC','field').split('~')
        if cp.has_option('DIAGNOSTIC','preproc') :
            diag_preprocs = cp.get('DIAGNOSTIC','preproc').split('~')
        if cp.has_option('DIAGNOSTIC','only') :
            diag_only = cp.get('DIAGNOSTIC','only').split('~')
        if cp.has_option('DIAGNOSTIC','scripts') :
            diag_scripts = cp.get('DIAGNOSTIC','scripts').split('~')
        if cp.has_option('DIAGNOSTIC','config_files') :
            diag_conf_files = cp.get('DIAGNOSTIC','config_files').split('~')
        # parse additional models
        if cp.has_option('ADDITIONAL_MODELS','names') :
            amodel_names = cp.get('ADDITIONAL_MODELS','names').split(',')
        if cp.has_option('ADDITIONAL_MODELS','projects') :
            amodel_projects = cp.get('ADDITIONAL_MODELS','projects').split(',')
        if cp.has_option('ADDITIONAL_MODELS','types') :
            amodel_types = cp.get('ADDITIONAL_MODELS','types').split(',')
        if cp.has_option('ADDITIONAL_MODELS','versions') :
            amodel_versions = cp.get('ADDITIONAL_MODELS','versions').split(',')
        if cp.has_option('ADDITIONAL_MODELS','starts') :
            amodel_starts = [int(a) for a in cp.get('ADDITIONAL_MODELS','starts').split(',')]
        if cp.has_option('ADDITIONAL_MODELS','ends') :
            amodel_ends = [int(a) for a in cp.get('ADDITIONAL_MODELS','ends').split(',')]
        if cp.has_option('ADDITIONAL_MODELS','paths') :
            amodel_paths = cp.get('ADDITIONAL_MODELS','paths').split(',')

        # construct a list of dictionaries for each diagnostic
        diagnostics = []
        for i in range(len(diag_ids)):
            DIA = {}
            DIA['id'] = diag_ids[i]
            DIA['tags'] = [a for a in diag_tags[i].split(',')]          
            DIA['variables'] = []
            for j in range(len(diag_vars[i].split(','))):
                vari = {}
                vari['name'] = diag_vars[i].split(',')[j]
                vari['ref_model'] = [a for a in diag_refs[i].split(',')]
                vari['field'] = diag_fields[i].split(',')[j]
                vari['preproc'] = diag_preprocs[i]
                vari['only'] = diag_only[i].split(',')[j]
                DIA['variables'].append(vari)
            DIA['scripts'] = []
            for k in range(len(diag_scripts[i].split(','))):
                diaS = {}
                diaS['script'] = diag_scripts[i].split(',')[k]
                diaS['cfg_file'] = diag_conf_files[i].split(',')[k]
                DIA['scripts'].append(diaS)
            #DIA['conf_files'] = [a for a in diag_conf_files[i].split(',')]
            DIA['additional_models'] = []
            for i in range(len(amodel_names)):
                adm = {}
                adm['name'] = amodel_names[i]
                adm['project'] = amodel_projects[i]
                adm['type'] = amodel_types[i]
                adm['version'] = amodel_versions[i]
                adm['start'] = amodel_starts[i]
                adm['end'] = amodel_ends[i]
                adm['path'] = amodel_paths[i]
                DIA['additional_models'].append(adm)
            diagnostics.append(DIA)
        if len(diagnostics) == 0:
            print >> sys.stderr, "No diagnostics specified in the Namelist file, exiting", params_file
            sys.exit(1)
        else:
            #for j in range(len(diagnostics)):
            #    print(diagnostics[j])
            return diagnostics

    def project_info(self, params_file):
        """
        Function to build the final dictionary to hold
        all parser information
        """
        ALL = {}
        ALL['GLOBAL'] = self.GLOBAL(params_file)
        ALL['PREPROCESS'] = self.PREPROCESS(params_file)
        ALL['MODELS'] = self.MODELS(params_file)
        ALL['DIAGNOSTICS'] = self.DIAGNOSTICS(params_file)
        return ALL

# testing area
pf = 'namelist.ini'
nm = Namelist()
for i in nm.project_info(pf)['DIAGNOSTICS'][0].items():
    print(i)
