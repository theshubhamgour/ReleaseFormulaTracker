import re
import json
from typing import List, Dict, Any
from datetime import datetime
import traceback

class StackGenerator:
    """
    Generates release image stacks based on Excel formulas and product versions
    """
    
    def __init__(self):
        self.component_mappings = {
            'VLOOKUP': {'type': 'studio-backend', 'category': 'lookup'},
            'HLOOKUP': {'type': 'studio-ui', 'category': 'lookup'},  
            'INDEX': {'type': 'bodhee-core', 'category': 'indexing'},
            'MATCH': {'type': 'file-upload-connector', 'category': 'matching'},
            'IF': {'type': 'bodhee-security', 'category': 'conditional'},
            'SUMIF': {'type': 'bxs-masterdata', 'category': 'aggregation'},
            'COUNTIF': {'type': 'bxs-masterdata-management', 'category': 'aggregation'},
            'CONCATENATE': {'type': 'studio-backend', 'category': 'formatting'},
            'SUM': {'type': 'bodhee-core', 'category': 'math'},
            'AVERAGE': {'type': 'studio-ui', 'category': 'math'},
            'MAX': {'type': 'bodhee-security', 'category': 'math'},
            'MIN': {'type': 'file-upload-connector', 'category': 'math'},
            'ROUND': {'type': 'bxs-masterdata', 'category': 'math'},
            'TODAY': {'type': 'bxs-masterdata-management', 'category': 'temporal'},
            'NOW': {'type': 'studio-backend', 'category': 'temporal'},
            'DATE': {'type': 'studio-ui', 'category': 'temporal'},
            'INDIRECT': {'type': 'bodhee-core', 'category': 'dynamic'},
            'OFFSET': {'type': 'bodhee-security', 'category': 'dynamic'},
            'CHOOSE': {'type': 'file-upload-connector', 'category': 'selection'},
            'SWITCH': {'type': 'bxs-masterdata', 'category': 'selection'},
            'TEXTJOIN': {'type': 'bxs-masterdata-management', 'category': 'formatting'},
            'FILTER': {'type': 'studio-backend', 'category': 'filtering'},
            'UNIQUE': {'type': 'studio-ui', 'category': 'deduplication'},
            'SORT': {'type': 'bodhee-core', 'category': 'ordering'},
            'ARITHMETIC': {'type': 'bodhee-security', 'category': 'basic-math'},
            'REFERENCE': {'type': 'file-upload-connector', 'category': 'basic'}
        }
        
        self.service_dependencies = {
            'data-service': ['database', 'cache'],
            'search-service': ['search-engine', 'cache'],
            'logic-service': ['rules-engine'],
            'calculation-service': ['compute-engine'],
            'text-service': ['text-processor'],
            'date-service': ['time-service'],
            'reference-service': ['reference-resolver']
        }
        
        self.base_infrastructure = [
            {'name': 'load-balancer', 'type': 'infrastructure', 'required': True},
            {'name': 'api-gateway', 'type': 'infrastructure', 'required': True},
            {'name': 'database', 'type': 'infrastructure', 'required': True},
            {'name': 'cache', 'type': 'infrastructure', 'required': False},
            {'name': 'monitoring', 'type': 'infrastructure', 'required': True},
            {'name': 'logging', 'type': 'infrastructure', 'required': True}
        ]
    
    def generate_stack(self, formulas: List[Dict[str, Any]], product_version: str, 
                      environment: str = "production", include_dependencies: bool = True,
                      validate_formulas: bool = True) -> Dict[str, Any]:
        """
        Generate a release image stack based on formulas and configuration
        
        Args:
            formulas: List of formula dictionaries from FormulaProcessor
            product_version: Product version string
            environment: Target environment
            include_dependencies: Whether to include service dependencies
            validate_formulas: Whether to validate formulas before processing
            
        Returns:
            Dictionary containing the generated stack information
        """
        try:
            result = {
                'success': False,
                'stack_version': self._generate_stack_version(product_version),
                'product_version': product_version,
                'environment': environment,
                'generated_at': datetime.now().isoformat(),
                'components': [],
                'configuration': {},
                'metadata': {}
            }
            
            # Validate formulas if requested
            if validate_formulas:
                validation_result = self._validate_formulas(formulas)
                result['validation'] = validation_result
                
                if validation_result['invalid_count'] > 0:
                    result['error'] = f"Found {validation_result['invalid_count']} invalid formulas"
                    return result
            
            # Analyze formulas to determine required components
            component_analysis = self._analyze_formula_requirements(formulas)
            result['metadata']['analysis'] = component_analysis
            
            # Generate components based on analysis
            components = self._generate_components(component_analysis, include_dependencies)
            result['components'] = components
            
            # Generate configuration
            configuration = self._generate_configuration(
                components, product_version, environment, formulas
            )
            result['configuration'] = configuration
            
            # Add metadata
            result['metadata'].update({
                'total_formulas': len(formulas),
                'unique_formula_types': len(set(f['formula_type'] for f in formulas)),
                'complexity_breakdown': self._get_complexity_breakdown(formulas),
                'sheets_processed': len(set(f['sheet'] for f in formulas))
            })
            
            result['success'] = True
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stack_version': self._generate_stack_version(product_version),
                'product_version': product_version,
                'environment': environment,
                'generated_at': datetime.now().isoformat()
            }
    
    def _generate_stack_version(self, product_version: str) -> str:
        """Generate a stack version based on product version"""
        # Extract version components
        version_match = re.match(r'v?(\d+)\.(\d+)\.(\d+)(?:-(.+))?', product_version)
        if version_match:
            major, minor, patch, pre = version_match.groups()
            if pre:
                return f"stack-{major}.{minor}.{patch}-{pre}"
            else:
                return f"stack-{major}.{minor}.{patch}"
        else:
            # Fallback for non-standard version formats
            clean_version = re.sub(r'[^a-zA-Z0-9.-]', '', product_version)
            return f"stack-{clean_version}"
    
    def _validate_formulas(self, formulas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate formulas for common issues"""
        validation_result = {
            'valid_count': 0,
            'invalid_count': 0,
            'errors': [],
            'warnings': []
        }
        
        for formula_info in formulas:
            formula = formula_info.get('formula', '')
            
            # Check for basic formula structure
            if not formula.startswith('='):
                validation_result['errors'].append(
                    f"Sheet '{formula_info['sheet']}', Cell {formula_info['cell']}: Formula doesn't start with '='"
                )
                validation_result['invalid_count'] += 1
                continue
            
            # Check for unmatched parentheses
            open_parens = formula.count('(')
            close_parens = formula.count(')')
            if open_parens != close_parens:
                validation_result['errors'].append(
                    f"Sheet '{formula_info['sheet']}', Cell {formula_info['cell']}: Unmatched parentheses"
                )
                validation_result['invalid_count'] += 1
                continue
            
            # Check for empty formulas
            if len(formula.strip()) <= 1:
                validation_result['errors'].append(
                    f"Sheet '{formula_info['sheet']}', Cell {formula_info['cell']}: Empty formula"
                )
                validation_result['invalid_count'] += 1
                continue
            
            # Check for potentially problematic references
            if '#REF!' in formula:
                validation_result['warnings'].append(
                    f"Sheet '{formula_info['sheet']}', Cell {formula_info['cell']}: Contains #REF! error"
                )
            
            validation_result['valid_count'] += 1
        
        return validation_result
    
    def _analyze_formula_requirements(self, formulas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze formulas to determine component requirements"""
        analysis = {
            'formula_types': {},
            'complexity_levels': {'low': 0, 'medium': 0, 'high': 0},
            'required_services': set(),
            'data_dependencies': set(),
            'processing_requirements': {}
        }
        
        for formula_info in formulas:
            formula_type = formula_info.get('formula_type', 'UNKNOWN')
            complexity = formula_info.get('complexity', 'unknown')
            
            # Count formula types
            analysis['formula_types'][formula_type] = analysis['formula_types'].get(formula_type, 0) + 1
            
            # Count complexity levels
            if complexity in analysis['complexity_levels']:
                analysis['complexity_levels'][complexity] += 1
            
            # Determine required services
            if formula_type in self.component_mappings:
                mapping = self.component_mappings[formula_type]
                analysis['required_services'].add(mapping['type'])
                
                # Analyze data dependencies
                references = formula_info.get('references', [])
                if references:
                    analysis['data_dependencies'].update(references)
                
                # Processing requirements based on complexity
                if complexity == 'high':
                    analysis['processing_requirements'][mapping['type']] = 'high-performance'
                elif complexity == 'medium':
                    analysis['processing_requirements'][mapping['type']] = 'standard'
        
        return analysis
    
    def _generate_components(self, analysis: Dict[str, Any], include_dependencies: bool) -> List[Dict[str, Any]]:
        """Generate stack components based on analysis"""
        components = []
        
        # Add base infrastructure
        for infra in self.base_infrastructure:
            components.append({
                'name': infra['name'],
                'type': infra['type'],
                'category': 'infrastructure',
                'required': infra['required'],
                'version': 'latest',
                'replicas': 1 if infra['name'] in ['database', 'monitoring', 'logging'] else 2
            })
        
        # Add application services based on formula analysis
        required_services = analysis.get('required_services', set())
        processing_requirements = analysis.get('processing_requirements', {})
        
        for service_type in required_services:
            component = {
                'name': service_type,
                'type': 'application',
                'category': 'service',
                'required': True,
                'version': 'latest',
                'replicas': 2
            }
            
            # Adjust replicas based on processing requirements
            if service_type in processing_requirements:
                if processing_requirements[service_type] == 'high-performance':
                    component['replicas'] = 3
                    component['resources'] = 'high'
                else:
                    component['resources'] = 'standard'
            
            components.append(component)
            
            # Add dependencies if requested
            if include_dependencies and service_type in self.service_dependencies:
                for dep in self.service_dependencies[service_type]:
                    # Check if dependency already exists
                    if not any(c['name'] == dep for c in components):
                        components.append({
                            'name': dep,
                            'type': 'dependency',
                            'category': 'support',
                            'required': True,
                            'version': 'latest',
                            'replicas': 1
                        })
        
        return components
    
    def _generate_configuration(self, components: List[Dict[str, Any]], 
                              product_version: str, environment: str,
                              formulas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate configuration for the stack"""
        config = {
            'deployment': {
                'strategy': 'rolling-update',
                'max_unavailable': '25%',
                'max_surge': '25%'
            },
            'networking': {
                'load_balancer': {
                    'algorithm': 'round_robin',
                    'health_check': '/health'
                },
                'api_gateway': {
                    'rate_limiting': '1000/min',
                    'timeout': '30s'
                }
            },
            'scaling': {
                'auto_scaling': environment == 'production',
                'min_replicas': 1,
                'max_replicas': 10,
                'cpu_threshold': 70,
                'memory_threshold': 80
            },
            'monitoring': {
                'metrics_enabled': True,
                'logging_level': 'INFO' if environment == 'production' else 'DEBUG',
                'alerts': environment == 'production'
            },
            'security': {
                'encryption_at_rest': environment == 'production',
                'encryption_in_transit': True,
                'authentication_required': True
            }
        }
        
        # Add formula-specific configuration
        formula_types = set(f['formula_type'] for f in formulas)
        
        if any(ft in ['VLOOKUP', 'HLOOKUP', 'INDEX', 'MATCH'] for ft in formula_types):
            config['data_services'] = {
                'cache_enabled': True,
                'cache_ttl': '1h',
                'index_optimization': True
            }
        
        if any(ft in ['SUM', 'AVERAGE', 'COUNT'] for ft in formula_types):
            config['calculation_services'] = {
                'parallel_processing': True,
                'result_caching': True,
                'precision': 'high'
            }
        
        if any(ft in ['TODAY', 'NOW', 'DATE'] for ft in formula_types):
            config['date_services'] = {
                'timezone': 'UTC',
                'date_format': 'ISO8601',
                'sync_enabled': True
            }
        
        return config
    
    def _get_complexity_breakdown(self, formulas: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of formula complexity levels"""
        breakdown = {'low': 0, 'medium': 0, 'high': 0, 'unknown': 0}
        
        for formula in formulas:
            complexity = formula.get('complexity', 'unknown')
            if complexity in breakdown:
                breakdown[complexity] += 1
        
        return breakdown
    
    def export_docker_compose(self, stack_result: Dict[str, Any]) -> str:
        """
        Export the stack as a Docker Compose file
        
        Args:
            stack_result: Result from generate_stack method
            
        Returns:
            Docker Compose YAML content as string
        """
        if not stack_result.get('success'):
            raise ValueError("Cannot export unsuccessful stack generation")
        
        compose_content = [
            "version: '3.8'",
            "",
            "services:"
        ]
        
        components = stack_result.get('components', [])
        
        for component in components:
            name = component['name'].replace('-', '_')
            compose_content.extend([
                f"  {name}:",
                f"    image: {component['name']}:latest",
                f"    deploy:",
                f"      replicas: {component['replicas']}"
            ])
            
            if component['type'] == 'infrastructure':
                if component['name'] == 'load-balancer':
                    compose_content.extend([
                        "    ports:",
                        "      - '80:80'",
                        "      - '443:443'"
                    ])
                elif component['name'] == 'database':
                    compose_content.extend([
                        "    ports:",
                        "      - '5432:5432'",
                        "    environment:",
                        "      - POSTGRES_DB=releasedb",
                        "      - POSTGRES_USER=admin",
                        "      - POSTGRES_PASSWORD=password"
                    ])
            
            compose_content.append("")
        
        return '\n'.join(compose_content)
